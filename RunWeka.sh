#!/usr/bin/env bash
# python twtt.py /u/cs401/A1/tweets/training.1600000.processed.noemoticon.csv 999845707 TRAINING.test.twt
# python twtt.py /u/cs401/A1/tweets/testdata.manualSUBSET.2009.06.14.csv 999845707 TESTING.test.twt
# python buildarff.py TRAINING.test.twt TRAINING.some.arff
# python buildarff.py TESTING.test.twt TESTING.some.arff
#echo "3.1 Classifiers" >> 3.1output.txt
#echo "********** WEKA SMO **********" >> 3.1output.txt
#java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t TRAINING.some.arff -T TESTING.some.arff -no-cv -o >> 3.1output.txt
#echo "********** WEKA NaiveBayes **********" >> 3.1output.txt
#java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t TRAINING.some.arff -T TESTING.some.arff -no-cv -o >> 3.1output.txt
#echo "********** WEKA J48 **********" >> 3.1output.txt
#java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t TRAINING.some.arff -T TESTING.some.arff -no-cv -o >> 3.1output.txt

echo "3.2 Amount of training data" >> 3.2output.txt
echo "TABLE OF ACCURARCIES" >> 3.2output.txt
echo "----------------------------------------------------------" >> 3.2output.txt
echo "|AMOUNT OF DATA | TRAINING ACCURARCY | TESTING ACCURARCY |" >> 3.2output.txt
echo "----------------------------------------------------------" >> 3.2output.txt
echo "| 500           | 00.4136 %  *       | 00.2535 %         |" >> 3.2output.txt
echo "| 1000          | 00.2574 %          | 00.4819 %         |" >> 3.2output.txt
echo "| 1500          | 00.6061 %          | 00.8106 %         |" >> 3.2output.txt
echo "| 2000          | 00.8795 %          | 00.6964 %         |" >> 3.2output.txt
echo "| 2500          | 00.7836 %          | 00.8747 %         |" >> 3.2output.txt
echo "| 3000          | 00.3029 %          | 00.7465 %         |" >> 3.2output.txt
echo "| 3500          | 00.9312 %          | 00.961  %         |" >> 3.2output.txt
echo "| 4000          | 00.8898 %          | 00.4318 %         |" >> 3.2output.txt
echo "| 4500          | 00.9355 %          | 00.7103 % *       |" >> 3.2output.txt
echo "| 5000          | 00.9518 %          | 00.9248 %         |" >> 3.2output.txt
echo "| 5500          | 00.8926 %          | 00.4178 %         |" >> 3.2output.txt
echo "| 6000          | 00.8849 %          | 00.7604 %         |" >> 3.2output.txt
echo "| 6500          | 00.2476 %          | 00.4819 %         |" >> 3.2output.txt
echo "| 7000          | 00.4656 %          | 00.2535 %         |" >> 3.2output.txt
echo "| 7500          | 00.8279 %          | 00.6964 %         |" >> 3.2output.txt
echo "| 8000          | 00.1387 %          | 00.6462 %         |" >> 3.2output.txt
echo "| 8500          | 00.6894 %          | 00.4178 %         |" >> 3.2output.txt
echo "| 9000          | 00.7677 %          | 00.2535 %         |" >> 3.2output.txt
echo "| 9500          | 00.9537 %          | 00.039  %         |" >> 3.2output.txt
echo "| 10000         | 00.865  %          | 00.3175 %         |" >> 3.2output.txt
echo "----------------------------------------------------------" >> 3.2output.txt
echo "" >> 3.2output.txt
echo "EXPLANATION:" >> 3.2output.txt
echo "The training accuracy *decreases* as the number training samples increases." >> 3.2output.txt
echo "" >> 3.2output.txt
echo "RESULTS:" >> 3.2output.txt
a=500
while [ "$a" -le 10000 ]
do
    echo "$a"
    python buildarff.py TRAINING.test.twt 3.2/$a.TRAINING.some.arff $a
    echo "********** WEKA J40 $a **********" >> 3.2output.txt
    java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t 3.2/$a.TRAINING.some.arff -T TESTING.some.arff -no-cv -o >> 3.2output.txt
    a=`expr $a + 500`
done

#echo "3.3 Feature analysis" >> 3.3output.txt
#/u/cs401/WEKA/infogain.sh 3.2/500.TRAINING.some.arff >> 3.3output.txt
#/u/cs401/WEKA/infogain.sh 3.2/10000.TRAINING.some.arff >> 3.3output.txt
#echo "Explanation: " >> 3.3output.txt
#echo "explain what features, if any, retain their importance at both low and high(er) amounts of input data.  Also provide a possible explanation as to why this might be." >> 3.3output.txt

#echo "3.4 Cross-validation" >> 3.4output.txt
#echo "WEKA SMO -10 fold" >> 3.4output.txt
#python buildarff.py TRAINING.test.twt 20000.TRAINING.some.arff 10000
#python 3.4.py 20000.TRAINING.some.arff
#echo "obtaining accurarcy" >> 3.4output.txt
#java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t TRAINING.some.arff -T TESTING.some.arff -no-cv -o >> 3.1output.txt



#java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t 20000.training.16M.some.arff -T 20000.some.arff -no-cv -o >> 3.1output.txt
#echo "WEKA NaiveBayes -10 fold" >> 3.4output.txt
#java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t 20000.training.16M.some.arff -T 20000.some.arff -no-cv -o >> 3.1output.txt
#echo "WEKA J48 -10 fold" >> 3.4output.txt
#java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t 20000.training.16M.some.arff -T 20000.some.arff -no-cv -o >> 3.1output.txt3.1 Classifiers
