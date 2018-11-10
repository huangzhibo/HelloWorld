import "https://raw.githubusercontent.com/huangzhibo/Learn/master/hello_world.wdl" as wh

workflow HelloWorld_SGE {

        #Array[Array[String]] inputSamples = read_tsv("/Users/huangzhibo/GitHub/wdl/test/slide_lane.tsv")
        Array[Array[String]] inputSamples = [["hello", "world"]] 
	call WriteGreeting {
	    input:slide=inputSamples[0]
	}
        call wh.WriteHello
}

task WriteGreeting {
        Array[String] slide

	command {
                echo ${slide[0]}
		echo "Hello World"
                echo "test123" >test
	}

	output {
		File outfile = stdout()
		File test = "test" 
	}
}
