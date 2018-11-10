task WriteHello {
	command {
		echo "Hello"
	}
	output {
		File outfile = stdout()
	}
}
