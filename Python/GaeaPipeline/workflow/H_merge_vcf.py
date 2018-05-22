# encoding: utf-8
import os

from gaeautils.bundle import bundle
from gaeautils.workflow import Workflow


class merge_vcf(Workflow):
    """ merge_vcf """

    INIT = bundle(merge_vcf=bundle())
    INIT.merge_vcf.program = "gaeatools.jar"
    INIT.merge_vcf.bcftools = ""
    INIT.merge_vcf.bcftools_param = ""
    INIT.merge_vcf.parameter = ""
    INIT.merge_vcf.parameter_check = ""
    INIT.merge_vcf.bed_list = ""

    def run(self, impl, dependList):
        impl.log.info("step: merge_vcf!")
        inputInfo = self.results[dependList[0]].output
        result = bundle(output=bundle(), script=bundle())

        if 'bed_list' in self.file:
            self.merge_vcf.bed_list = self.expath('file.bed_list')

        # extend program path
        self.merge_vcf.program = self.expath('merge_vcf.program')
        self.merge_vcf.bed_list = self.expath('merge_vcf.bed_list')
        self.merge_vcf.bcftools = self.expath('merge_vcf.bcftools', False)

        # global param
        hadoop_parameter = ' -D mapreduce.job.name="gaeaHC_merge_vcf" '
        if self.hadoop.get('queue'):
            hadoop_parameter += ' -D mapreduce.job.queuename={} '.format(self.hadoop.queue)

        ParamDict = {
            "PROGRAM": "%s jar %s SortVcf" % (self.hadoop.bin, self.merge_vcf.program),
            "HADOOPPARAM": hadoop_parameter
        }

        JobParamList = []
        for sampleName in inputInfo:
            scriptsdir = impl.mkdir(self.gaeaScriptsDir, sampleName)
            outputPath = impl.mkdir(self.option.workdir, "variation", sampleName)
            result.output[sampleName] = os.path.join(outputPath, "{}.hc.vcf.gz".format(sampleName))
            gvcf = os.path.join(outputPath, "{}.g.vcf.gz".format(sampleName))

            #global param
            JobParamList.append({
                    "SAMPLE" : sampleName,
                    "SCRDIR" : scriptsdir,
                    "INPUT" : inputInfo[sampleName],
                    "VCFDIR" : os.path.join(inputInfo[sampleName], 'pure_part_vcf_dir'),
                    "GVCFDIR" : os.path.join(inputInfo[sampleName], 'pure_part_gvcf_dir'),
                    "VCF": result.output[sampleName],
                    "GVCF": gvcf
                })
   
        cmd = ["source %s/bin/activate" % self.GAEA_HOME,
               'check_hc_part.py -b %s -p ${INPUT} -o ${VCFDIR}' % self.merge_vcf.bed_list,
               'if [ $? != 0 ]\nthen',
               '\texit 1',
               'fi',
               '${PROGRAM} ${HADOOPPARAM} -input file://${VCFDIR} -output file://${VCF} &\n',
               'check_hc_part.py -b %s -p ${INPUT} -o ${GVCFDIR} -s .g.vcf.gz' % self.merge_vcf.bed_list,
               'if [ $? != 0 ]\nthen',
               '\texit 1',
               'fi',
               '${PROGRAM} ${HADOOPPARAM} -input file://${GVCFDIR} -output file://${GVCF}',
               'wait\n'
               ]
        if self.merge_vcf.bcftools:
            cmd.append("%s index %s ${VCF}" % (self.merge_vcf.bcftools, self.merge_vcf.bcftools_param))
            cmd.append("%s index %s ${GVCF}" % (self.merge_vcf.bcftools, self.merge_vcf.bcftools_param))

        #write script
        scriptPath = \
        impl.write_scripts(
                name = 'merge_vcf',
                commands=cmd,
                JobParamList=JobParamList,
                paramDict=ParamDict)

        # result
        result.script.update(scriptPath)
        return result
