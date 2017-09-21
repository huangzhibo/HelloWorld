from gaeautils import bundle, Logger
import glob
import os


logger = Logger('log.txt','2',"mode6",True).getlog()
def parse_sample(sampleList):
    total_number = 0
    sampleInfo = bundle()
    with open(sampleList,'r') as f:
        for line in f:
            line = line.strip()
            field = line.split()
            sampleName = field[1]
            fq_dir = field[-1].strip()
            fq1s = glob.glob("%s/*1.fq.gz" % fq_dir)

            if len(fq1s) == 0:
                logger.error("fq1 under %s don't exists." % sampleName)
                exit(3)

            for fq1 in fq1s:
                total_number += 1
                fq_dir = os.path.abspath(os.path.dirname(fq1))
                fq_name = os.path.basename(fq1)

                # slideID_laneID_barcode
                # CL100035764_L02_33_1.fq.gz
                tmp = fq_name.split("_")
                rg_LB = field[2]
                rg_ID = "{}_{}_{}_{}".format(sampleName, tmp[0], tmp[1], tmp[2])
                rg_PU = tmp[0] + "_" + tmp[1] + "_" + tmp[2]
                rg = "@RG\\tID:%s\\tPL:COMPLETE\\tPU:%s\\tLB:%s\\tSM:%s\\tCN:BGI" % (rg_ID, rg_PU, rg_LB, sampleName)
                fq_lib_name = rg_ID

                if not sampleInfo.has_key(sampleName):
                        sampleInfo[sampleName] = bundle()
                        sample_lane_counter = 0
                else:
                    sample_lane_counter = len(sampleInfo[sampleName])

                dataTag = 'data'+str(sample_lane_counter)
                if not sampleInfo[sampleName].has_key(dataTag):
                    sampleInfo[sampleName][dataTag] = bundle()

                sampleInfo[sampleName][dataTag]['fq1'] = fq1

                #find fq2
                fq2 = fq1
                fq2 = fq2.replace("1.fq.gz", "2.fq.gz")
                if os.path.exists(fq2):
                    sampleInfo[sampleName][dataTag]['fq2'] = fq2
                else:
                    logger.warning("%s of line: %d is SE data!" % (sampleName,total_number))

                sampleInfo[sampleName][dataTag]['rg'] = rg
                sampleInfo[sampleName][dataTag]['libname'] = fq_lib_name
                sampleInfo[sampleName][dataTag]['gender'] = 'male'
            
    return sampleInfo
