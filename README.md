# Efficient mining of association rules using closed itemset lattices

The goal of this project is to generate association rules using closed itemset lattices.
We first generate closed frequent itemsets using CHARM algorithm, then mine all frequent 
itemsets and finally generate strong association rules from the output. 

Requirements:
- Python 3.7 to run AssociationRules.py as executable program
- Provided text file which holds database form where association rules are to be mined
- re library

Execution:
As to run program and find strong associations rules user is aksed to provide text file that hold database.
Text file must be in the same folder where CHARM.py is run. Text file must be written in the given format:
n) <item_1_i>, <item_2_i>, ..., <item_m_i>
n - number of the transactionID
item_m_i - in i-th row and m-th column
After execution of program user is asked to write name of the text file and give 3 values:

  minSupCharm <1,n> - integer defining minimal support for the frequent itemsets
  minSupRules <0,1> - float definig minimal support for the association rules
  minConf <0,n> - float defining minimal confidence for the association rules

