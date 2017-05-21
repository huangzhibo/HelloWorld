#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import commands
import subprocess
import re
import time
import json
import xml.etree.ElementTree as ET
from glob import glob
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__version__ = '1.0.0'
__date__ = '2017-02-08'
__updated__ = '2017-02-08'


def search_file(search_path, pattern):
    for match in glob(os.path.join(search_path, pattern)):
        return match


def check_job(jobid_list):
    for jobid in jobid_list:
        n = commands.getoutput("yhqueue -j {0} |grep {0}".format(str(jobid)))
        if not n or n.find('Invalid job id specified') != -1:
            return False
        else:
            return True


class ThCluster(object):
    def __init__(self, state=None):
        if state is None:
            self.scancel_sh = ''
            self.hadoop_cfg = ''
            self.cluster_dir = ''
            self.slurm_sinfo = 'yhinfo'
            self.partition = ''
            self.hadoop = ''
            self.streaming_jar = ''
            self.hadoop_pkg = ''
            self.hadoop_version = ''
            self.source_dir = ''
            self.idle_node_list_str = ''
            self.master_node = ''
            self.master_hadoop_dir = ''
            self.slave_node_list = []
            self.finished_alloc_node_list = []
            self.alloc_node_jobid = []
            self.alloc_node_done = True
        else:
            self.__dict__.update(state)

    def parse_node_info(self):
        n = commands.getoutput("{} |grep {} | grep idle".format(self.slurm_sinfo, self.partition))
        if not n:
            print "No idle node!"
            exit(1)
        fields = n.split()
        self.idle_node_list_str = fields[5]
        return self._extend_node_str()

    def _extend_node_str(self):
        idle_node_list = []
        if self.idle_node_list_str != '':
            index = self.idle_node_list_str.find('[')
            if index == -1:
                idle_node_list.append(self.idle_node_list_str)
            else:
                node_tag = self.idle_node_list_str[:index]
                id_strs = self.idle_node_list_str[index + 1:-1]
                id_str_list = id_strs.split(',')
                for id_str in id_str_list:
                    if id_str.find('-') == -1:
                        idle_node_list.append(node_tag + id_str)
                        continue
                    (start, end) = id_str.split('-')
                    i = int(start)
                    while i <= int(end):
                        idle_node_list.append(node_tag + str(i))
                        i += 1
        return idle_node_list

    def set_source_dir(self, source_dir):
        self.source_dir = os.path.abspath(source_dir)
        self.hadoop_pkg = search_file(self.source_dir, 'hadoop*.tar.gz')
        p1 = r"hadoop-(.*).tar.gz"
        pattern = re.compile(p1)
        m = re.search(pattern, os.path.basename(self.hadoop_pkg))
        if m:
            self.hadoop_version = m.group(1)
        else:
            print "hadoop program is wrong!"
        print "hadoop version is {}".format(self.hadoop_version)

    # submit get_ssh.sh
    def alloc_node(self, num=None, partition=None, node_list=None):
        if partition is not None:
            self.partition = partition
        if node_list is None:
            node_list = self.parse_node_info()

        self.alloc_node_jobid = []
        self.finished_alloc_node_list = []
        self.alloc_node_done = False

        get_ssh = os.path.join(self.source_dir, 'get_ssh.sh')

        p_list = []
        for n, node in enumerate(node_list):
            if num is not None and n >= num:
                break

            self.finished_alloc_node_list.append(node)
            p = subprocess.Popen("yhbatch -w {} -p {} {}".format(node, self.partition, get_ssh), shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p_list.append(p)

        for index, p in enumerate(p_list):
            for line in p.stdout.readlines():
                print line[:-1]
                pattern = re.compile(r'^Submitted batch job (\d+)')
                jobInfo = re.search(pattern, line)
                if jobInfo:
                    self.alloc_node_jobid.append(jobInfo.group(1))
                    break
                else:
                    print "Failed when alloc node: {}. ".format(self.finished_alloc_node_list[index])
                    self.finished_alloc_node_list.remove(index)

            for line in p.stderr.readlines():
                print 'ERROR: ' + line
            p.wait()
            if not self.alloc_node_jobid:
                exit(1)

        self.master_node = self.finished_alloc_node_list[0]
        self.slave_node_list = self.finished_alloc_node_list[1:]

        print "Alloc node ..."
        print ','.join(self.finished_alloc_node_list)

        self.scancel_sh = os.path.join(self.cluster_dir, "scancel.sh")
        with open(self.scancel_sh, "w") as scancel:
            scancel.write("#!/bin/sh\n")
            scancel.write("scancel\t{}\n".format('\t'.join(self.alloc_node_jobid)))
        os.chmod(self.scancel_sh, 0755)

    # 确保get_ssh.sh已经在执行
    def check_alloc_node(self):
        n = 0
        unalloc_node_list = list(self.finished_alloc_node_list)
        while len(unalloc_node_list):
            if n > 10:
                print "Alloc node failed!"
                exit(1)
            n += 1
            time.sleep(10)
            for node in unalloc_node_list:
                field = commands.getoutput("{sinfo} -n {N}|grep {N}".format(sinfo=self.slurm_sinfo, N=node)).split()
                print node, field
                if not field:
                    print "{sinfo} -n {N}|grep {N}".format(sinfo=self.slurm_sinfo, N=node)
                elif field[4] == 'alloc':
                    unalloc_node_list.remove(node)
        print "Alloc node completed!"
        self.alloc_node_done = True

    def copy_hadoop_package(self, cluster_dir):
        self.cluster_dir = cluster_dir
        print "copy hadoop program ..."
        p_list = []
        for node in self.finished_alloc_node_list:
            node_dir = os.path.join(cluster_dir, node)
            if not os.path.exists(node_dir):
                os.mkdir(node_dir)
                p = subprocess.Popen("tar -zxf {} -C {}".format(self.hadoop_pkg, node_dir), shell=True)
                p_list.append(p)
            tmp = os.path.join(node_dir, "tmp")
            if os.path.exists(tmp):
                os.removedirs(tmp)
            os.mkdir(tmp)
            os.chmod(tmp, 0777)

        for p in p_list:
            p.wait()

        hadoop_porgram_dirname = "hadoop-{}".format(self.hadoop_version)
        master_dir = os.path.join(cluster_dir, self.master_node)
        self.master_hadoop_dir = os.path.join(master_dir, hadoop_porgram_dirname)
        conf_dir = os.path.join(self.master_hadoop_dir, 'etc/hadoop')

        coreConfET = ConfigurationET(file=os.path.join(self.source_dir, 'core-site.xml'))
        hdfsConfET = ConfigurationET(file=os.path.join(self.source_dir, 'hdfs-site.xml'))
        yarnConfET = ConfigurationET(file=os.path.join(self.source_dir, 'yarn-site.xml'))
        mapredConfET = ConfigurationET(file=os.path.join(self.source_dir, 'mapred-site.xml'))

        coreConfET.addProperty('fs.defaultFS', "hdfs://{}:8020".format(self.master_node))
        coreConfET.addProperty('hadoop.tmp.dir', "{}/tmp".format(master_dir))
        coreConfET.indent()
        coreConfET.write(os.path.join(conf_dir, 'core-site.xml'))

        hdfsConfET.addProperty('dfs.namenode.name.dir', "file://{}/tmp/hdfs/nn".format(master_dir))
        hdfsConfET.addProperty('dfs.namenode.servicerpc-address', "{}:8022".format(self.master_node))
        hdfsConfET.addProperty('dfs.https.address', "{}:50470".format(self.master_node))
        hdfsConfET.addProperty('dfs.namenode.http-address', "{}:50070".format(self.master_node))
        hdfsConfET.addProperty('dfs.namenode.secondary.http-address', "{}:50090".format(self.master_node))
        hdfsConfET.indent()
        hdfsConfET.write(os.path.join(conf_dir, 'hdfs-site.xml'))

        yarnConfET.addProperty('yarn.resourcemanager.address', "{}:8032".format(self.master_node))
        yarnConfET.addProperty('yarn.resourcemanager.scheduler.address', "{}:8030".format(self.master_node))
        yarnConfET.addProperty('yarn.resourcemanager.resource-tracker.address', "{}:8031".format(self.master_node))
        yarnConfET.addProperty('yarn.resourcemanager.admin.address', "{}:8033".format(self.master_node))
        yarnConfET.addProperty('yarn.resourcemanager.webapp.address', "{}:8088".format(self.master_node))
        yarnConfET.indent()
        yarnConfET.write(os.path.join(conf_dir, 'yarn-site.xml'))

        mapredConfET.addProperty('mapreduce.job.reduces', str(len(self.slave_node_list) * 5 - 1))
        mapredConfET.addProperty('mapreduce.jobhistory.address', "{}:10020".format(self.master_node))
        mapredConfET.addProperty('mapreduce.jobhistory.webapp.address', "{}:19888".format(self.master_node))
        mapredConfET.addProperty('mapreduce.jobhistory.webapp.https.address', "{}:19890".format(self.master_node))
        mapredConfET.addProperty('mapreduce.jobhistory.admin.address', "{}:10033".format(self.master_node))
        mapredConfET.indent()
        mapredConfET.write(os.path.join(conf_dir, 'mapred-site.xml'))

        # edit masters file
        masters = os.path.join(conf_dir, 'masters')
        with open(masters, 'w') as m:
            m.write(self.master_node + '\n')

        # edit slaves file
        slaves = os.path.join(conf_dir, 'slaves')
        with open(slaves, 'w') as s:
            for node in self.slave_node_list:
                s.write(node + '\n')

        # edit hadoop-env.sh
        hadoop_env_path = os.path.join(conf_dir, 'hadoop-env.sh')
        with open(hadoop_env_path, 'a') as hadoop_env:
            if not os.getenv('JAVA_HOME'):
                print "No environment variable JAVA_HOME, please set it!"
                exit(1)
            hadoop_env.write("export JAVA_HOME={JH}\n".format(JH=os.getenv('JAVA_HOME')))
            hadoop_env.write("export CLASSPATH={JH}/lib:{JH}/jre/lib:.\n".format(JH=os.getenv('JAVA_HOME')))
            hadoop_env.write("export PATH=$PATH:{JH}/bin:{JH}/jre/bin\n".format(JH=os.getenv('JAVA_HOME')))
            native = os.path.join(self.master_hadoop_dir, 'lib/native')
            hadoop_env.write("export LD_LIBRARY_PATH={}\n".format(native))
            hadoop_env.write("export HADOOP_HEAPSIZE=4000\n")

        # edit slaves.sh
        master_slaves = os.path.join(self.master_hadoop_dir, 'sbin/slaves.sh')
        os.system("cp {} {}".format(os.path.join(self.source_dir, 'slaves.sh'), master_slaves))
        os.system("sed -i 's/master_node/{}/' {}".format(self.master_node, master_slaves))

        for node in self.slave_node_list:
            node_dir = os.path.join(cluster_dir, node)
            conf_dir = os.path.join(node_dir, hadoop_porgram_dirname, 'etc/hadoop')
            os.system("cp {} {}".format(hadoop_env_path, conf_dir))
            os.system("cp {} {}".format(master_slaves, os.path.join(node_dir, hadoop_porgram_dirname, 'sbin')))
            os.system("cp {} {}".format(masters, conf_dir))
            os.system("cp {} {}".format(slaves, conf_dir))

            coreConfET.addProperty('hadoop.tmp.dir', "{}/tmp".format(node_dir))
            # coreConfET.indent()
            coreConfET.write(os.path.join(conf_dir, 'core-site.xml'))
            hdfsConfET.write(os.path.join(conf_dir, 'hdfs-site.xml'))
            yarnConfET.write(os.path.join(conf_dir, 'yarn-site.xml'))
            mapredConfET.write(os.path.join(conf_dir, 'mapred-site.xml'))

        print "copy hadoop program completed!"
        self.hadoop = os.path.join(self.master_hadoop_dir, 'bin/hadoop')
        self.streaming_jar = \
            os.path.join(self.master_hadoop_dir,
                         'share/hadoop/tools/lib/hadoop-streaming-{version}.jar'.format(version=self.hadoop_version))

    def start_hadoop(self, namenode_format=True):
        start_dfs = os.path.join(self.master_hadoop_dir, 'sbin/start-dfs.sh')
        start_yarn = os.path.join(self.master_hadoop_dir, 'sbin/start-yarn.sh')
        start_history = os.path.join(self.master_hadoop_dir, 'sbin/mr-jobhistory-daemon.sh')

        if not self.alloc_node_done:
            self.check_alloc_node()
        hdfs = os.path.join(self.master_hadoop_dir, 'bin/hdfs')
        if namenode_format:
            p = subprocess.Popen("ssh {} {} namenode -format".format(self.master_node, hdfs), shell=True)
            p.wait()

        subprocess.call("ssh {} {}".format(self.master_node, start_dfs), shell=True)
        time.sleep(20)
        subprocess.call("ssh {} {}".format(self.master_node, start_yarn), shell=True)
        subprocess.call("ssh {} {} start historyserver".format(self.master_node, start_history), shell=True)
        if namenode_format:
            subprocess.call("{} dfs -chmod 777 /user".format(hdfs), shell=True)
            subprocess.call("{} dfs -chmod -R 777 /user/history".format(hdfs), shell=True)

        print "Hadoop has been started!"

    def stop_hadoop(self, release_node=True):
        if release_node:
            subprocess.call("sh {}".format(self.scancel_sh), shell=True)
            print "hadoop cluster has been killed! [{}]".format(self.cluster_dir)
        else:
            stop_dfs = os.path.join(self.master_hadoop_dir, 'sbin/stop-dfs.sh')
            stop_yarn = os.path.join(self.master_hadoop_dir, 'sbin/stop-yarn.sh')
            history_daemon = os.path.join(self.master_hadoop_dir, 'sbin/mr-jobhistory-daemon.sh')
            subprocess.call("ssh {} {}".format(self.master_node, stop_dfs), shell=True)
            subprocess.call("ssh {} {}".format(self.master_node, stop_yarn), shell=True)
            subprocess.call("ssh {} {} stop historyserver".format(self.master_node, history_daemon), shell=True)

    # 保存当前hadoop节点数目及节点列表
    def save_cluster_state(self):
        self.hadoop_cfg = os.path.join(self.cluster_dir, "hadoop.cfg")
        with open(self.hadoop_cfg, 'w') as cfg:
            cfg.write("[hadoop]\n")
            cfg.write("\tbin = {}\n".format(self.hadoop))
            cfg.write("\tstreamingJar = {}\n".format(self.streaming_jar))
            cfg.write("\tishadoop2 = true\n")
            cfg.write("\tis_at_TH = true\n")
            cfg.write("\tinput_format = file\n")
            cfg.write("\tfs_mode = hdfs\n")
            cfg.write("\tmapper_num = {}\n".format(str(len(self.slave_node_list) * 5 - 1)))
            cfg.write("\treducer_num = {}\n".format(str(len(self.slave_node_list) * 5 - 1)))

        cluster_state = os.path.join(self.cluster_dir, "cluster.json")
        with open(cluster_state, 'w') as cl:
            json.dump(self.__dict__, cl, indent=2)


class ConfigurationET(ET.ElementTree):
    def __init__(self, element=None, file=None):
        super(ConfigurationET, self).__init__(element, file)

    def getDict(self):
        key_value_dict = {}
        for property_node in self.findall("property"):
            key_value_dict[property_node.find("name").text] = property_node.find("value").text
        return key_value_dict

    def addProperty(self, key, value):
        for property_node in self.findall("property"):
            if property_node.find("name").text == key:
                property_node.find("value").text = value
                return

        property_node = ET.SubElement(self.getroot(), "property")
        name_node = ET.SubElement(property_node, "name")
        value_node = ET.SubElement(property_node, "value")
        name_node.text = key
        value_node.text = value

    def removeProperty(self, key):
        for property_node in self.findall("property"):
            if property_node.find("name").text == key:
                self.getroot().remove(property_node)

    def update(self, newDict):
        """

        :type newDict: dict
        """
        if not newDict:
            return

        for property_node in self.findall("property"):
            if property_node.find("name").text in newDict:
                property_node.find("value").text = newDict.get(property_node.find("name").text)
                newDict.pop(property_node.find("name").text)

        for key in newDict:
            property_node = ET.SubElement(self.getroot(), "property")
            name_node = ET.SubElement(property_node, "name")
            value_node = ET.SubElement(property_node, "value")
            name_node.text = key
            value_node.text = newDict.get(key)

    def indent(self, elem=None, level=0):
        i = "\n" + level * "  "
        if elem is None:
            elem = self.getroot()
        if len(elem):
            if elem.text is None or not elem.text.strip():
                elem.text = i + "  "
            if elem.tail is None or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if elem.tail is None or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (elem.tail is None or not elem.tail.strip()):
                elem.tail = i


def start_hadoop(args):
    args.cluster_dir = os.path.abspath(args.cluster_dir)
    if not os.path.exists(args.cluster_dir):
        os.mkdir(args.cluster_dir)
    else:
        print "cluster already exists!"
        return

    cluster = ThCluster()
    cluster.set_source_dir(args.source_dir)
    cluster.alloc_node(args.node_num, args.partition)
    print "master node is {}".format(cluster.master_node)

    cluster.copy_hadoop_package(args.cluster_dir)
    cluster.start_hadoop()
    cluster.save_cluster_state()


def restart_hadoop(args):
    cluster_state = os.path.join(args.cluster_dir, "cluster.json")
    with open(cluster_state, 'r') as cl:
        state = json.loads(cl.read())
        cluster = ThCluster(state)

        print cluster.alloc_node_jobid
        if check_job(cluster.alloc_node_jobid):
            cluster.stop_hadoop(False)
            cluster.start_hadoop(False)
        else:
            cluster.alloc_node(node_list=cluster.finished_alloc_node_list)
            cluster.start_hadoop(False)
            cluster.save_cluster_state()


def stop_hadoop(args):
    cluster_state = os.path.join(args.cluster_dir, "cluster.json")
    if not os.path.exists(cluster_state):
        print "{0} is not exists!".format(cluster_state)
    with open(cluster_state, 'r') as cl:
        state = json.loads(cl.read())
        cluster = ThCluster(state)
        for jobid in cluster.alloc_node_jobid:
            subprocess.call("yhcancel {}".format(jobid), shell=True)
            # cluster.stop_hadoop()


def main():
    program_name = os.path.basename(sys.argv[0])
    program_license = '''{0}
      Created by huangzhibo on {1}.
      Last updated on {2}.
      Copyright 2017 BGI bigData. All rights reserved.
    USAGE'''.format(" v".join([program_name, __version__]), str(__date__), str(__updated__))

    parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(title='subcommands', help='sub-command help')
    parser_start = subparsers.add_parser('start', help='start hadoop cluster')
    parser_restart = subparsers.add_parser('restart', help='restart hadoop cluster')
    parser_stop = subparsers.add_parser('stop', help='stop hadoop cluster')

    parser_start.add_argument("-n", "--node_number", dest="node_num", default=10, type=int,
                              help='number of nodes to run hadoop service [10] .')
    parser_start.add_argument("-d", "--cluster_dir", dest="cluster_dir",
                              help='directory to deploy hadoop cluster')
    parser_start.add_argument("-s", "--source_dir", dest="source_dir",
                              help='dir contains conf and hadoop program package(.tar.gz).')
    parser_start.add_argument("-p", "--partition", dest="partition", default='bgi_gd',
                              help='Only the node in these partitions can be used.')
    parser_start.set_defaults(func=start_hadoop)

    parser_restart.add_argument("cluster_dir", help='directory to deploy hadoop cluster')
    parser_restart.set_defaults(func=restart_hadoop)

    parser_stop.add_argument("cluster_dir", help='directory to deploy hadoop cluster')
    parser_stop.set_defaults(func=stop_hadoop)

    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    args = parser.parse_args()

    if sys.argv[1] == 'start':
        if not args.cluster_dir:
            parser_start.print_help()
            exit(0)
        if not args.source_dir:
            parser_start.print_help()
            exit(0)

    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
