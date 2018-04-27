# encoding: utf-8
import os

from gaeautils.bundle import bundle
from gaeautils.workflow import Workflow


class BwaMarkDupSpark(Workflow):
    """ BwaMarkDupSpark """

    INIT = bundle(BwaMarkDupSpark=bundle())
    INIT.BwaMarkDupSpark.program = "/hwfssz1/BIGDATA_COMPUTING/software/source/gatk4/gatk"
    INIT.BwaMarkDupSpark.parameter = '--bam-partition-size 10485760 --disable-sequence-dictionary-validation true --sharded-output true -- ' \
                                     '--spark-runner SPARK --spark-master yarn --executor-memory 30g --executor-cores 4 --driver-memory 30g ' \
                                     '--conf spark.shuffle.blockTransferService=nio '

    def run(self, impl, dependList):
        impl.log.info("step: BwaMarkDupSpark!")
        inputInfo = self.results[dependList[0]].output
        result = bundle(output=bundle(), script=bundle())

        # extend program path
        self.BwaMarkDupSpark.program = self.expath('BwaMarkDupSpark.program')

        # script template
        fs_cmd = self.fs_cmd
        cmd = []
        cmd.append("%s ${OUTPUT}" % fs_cmd.delete)
        cmd.append("%s ${INPUT}/*/_SUCCESS ${INPUT}/*/_logs" % fs_cmd.delete)
        cmd.append("${PROGRAM} BwaAndMarkDuplicatesPipelineSpark -I ${INPUT} -O ${OUTPUT} -R ${REF} ${PARAM}")

        for sampleName in inputInfo:
            scriptsdir = impl.mkdir(self.gaeaScriptsDir, sampleName)
            hdfs_outputPath = os.path.join(self.option.dirHDFS, sampleName, 'BwaMarkDupSpark_output.bam')

            # global param
            ParamDict = {
                "PROGRAM": self.BwaMarkDupSpark.program,
                "INPUT": 'hdfs:'+inputInfo[sampleName],
                "OUTPUT": hdfs_outputPath,
                "REF": "/hwfssz1/BIGDATA_COMPUTING/GaeaProject/reference/hg19/hg19.fasta.2bit",
                "PARAM": self.BwaMarkDupSpark.parameter
            }

            # write script
            scriptPath = \
                impl.write_shell(
                    name='BwaMarkDupSpark',
                    scriptsdir=scriptsdir,
                    commands=cmd,
                    paramDict=ParamDict)

            # result
            result.output[sampleName] = os.path.join(hdfs_outputPath, 'Mark')
            result.script[sampleName] = scriptPath
        return result

