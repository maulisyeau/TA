#!/bin/bash

# ARGUMENT INFORMATION
# First argument: File containing first sentences in input sentence pairs
# Second argument: File containing second sentences in input sentence pairs
# Third argument: Whether input sentences are chunked or not (True / False)
# Notice that all arguments are required

# EXAMPLES
#
# text_chunked = True
# ./01_run_baseline_aligner.sh STSint.input.headlines.sent1.chunk.txt STSint.input.headlines.sent2.chunk.txt True
#
# text_chunked = False
# redirect output to file to avoid processing info
# ./01_run_baseline_aligner.sh STSint.input.headlines.sent1.txt STSint.input.headlines.sent2.txt False

if [ $# -ne 3 ]
then
    # with wrong arguments execute help    
    #python iSTS16_task2_baseline.py --help
	python TA.py --help
    exit 1
fi

if [ ! -e $1 ]
then 
    echo "First argument file '$1' does not exist"
    exit -1
fi

if [ ! -e $2 ]
then 
    echo "Second argument file '$2' does not exist"
    exit -1
fi

if [ $3 != "True" -a $3 != "False" ]
then 
    echo "Third argument must be True/False"
    exit -1
fi

#python iSTS16_task2_baseline.py --sent1 $1 --sent2 $2 --chunked $3
python TA.py --sent1 $1 --sent2 $2 --chunked $3
