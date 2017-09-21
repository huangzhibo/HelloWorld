# encoding: utf-8
import os

from gaeautils.bundle import bundle
from gaeautils.workflow import Workflow


class haplotypeCaller(Workflow):
    """ haplotypeCaller """

    INIT = bundle(haplotypeCaller=bundle())
    INIT.haplotypeCaller.program = "GenomeAnalysisTK.jar"
    INIT.haplotypeCaller.parameter = "-rf BadCigar -ERC GVCF"
    INIT.haplotypeCaller.index_program = ""
    INIT.haplotypeCaller.mem = "40960"

    def run(self, impl, dependList):
        impl.log.info("step: haplotypeCaller!")
        inputInfo = self.results[dependList[0]].output
        result = bundle(output=bundle(), script=bundle())

        # extend program path
        self.haplotypeCaller.program = self.expath('haplotypeCaller.program')
        self.haplotypeCaller.index_program = self.expath('haplotypeCaller.index_program', False)

        if self.file.get("regionVariation"):
            self.haplotypeCaller.parameter += " -L %s " % self.file.regionVariation
        elif self.file.get("region"):
            self.haplotypeCaller.parameter += " -L %s " % self.file.region

        # global param
        ParamDict = self.file.copy()
        ParamDict.update({
            "PROGRAM": "java -Xmx{}m -jar {} ".format(self.haplotypeCaller.mem, self.haplotypeCaller.program),
            "REF": self.ref.normal.ref
        })

        # script template
        cmd = []
        if self.haplotypeCaller.get('index_program'):
            cmd.append('if [ ! -e ${INPUT}.bai ]\nthen')
            cmd.append('%s index ${INPUT}' % self.haplotypeCaller.index_program)
            cmd.append('fi')
        cmd.append("${PROGRAM} -T HaplotypeCaller -I ${INPUT} -o ${GVCF} -R ${REF} %s" % self.haplotypeCaller.parameter)
        # cmd.append("${PROGRAM} -T HaplotypeCaller --sample_name ${SAMPLE} -I ${INPUT} -o ${GVCF} -R ${REF} %s" % self.haplotypeCaller.parameter)
        cmd.append("${PROGRAM} -T GenotypeGVCFs -R ${REF} --variant ${GVCF} -o ${VCF}")

        JobParamList = []
        for sampleName in inputInfo:
            scriptsdir = impl.mkdir(self.option.workdir,"scripts",'standalone',sampleName)
            outputPath = impl.mkdir(self.option.workdir, "variation", 'haplotypeCaller', sampleName)
            result.output[sampleName] = os.path.join(outputPath, "{}.hc.vcf.gz".format(sampleName))
            gvcf = os.path.join(outputPath, "{}.hc.g.vcf.gz".format(sampleName))

            # global param
            JobParamList.append({
                "SAMPLE": sampleName,
                "SCRDIR": scriptsdir,
                "INPUT": inputInfo[sampleName],
                "VCF": result.output[sampleName],
                "GVCF": gvcf
            })

        # write script
        scriptPath = \
            impl.write_scripts(
                name='haplotypeCaller',
                commands=cmd,
                JobParamList=JobParamList,
                paramDict=ParamDict)

        # result
        result.script.update(scriptPath)
        return result
