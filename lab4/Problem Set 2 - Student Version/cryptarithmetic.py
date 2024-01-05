from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).

        problem.variables = []
        problem.domains = {}
        problem.constraints = []
     
         # get all the unique chars
        all_characters = set(LHS0 + LHS1 + RHS)
        

      # to keep the carry in it
        aux = []
        problem.variables = list(all_characters)
        # problem.domains = {var: [i for i in range(10)] for var in problem.variables}
        problem.constraints = []
        # no one can equal the other unique if they are variables not carries !
        for variable1 in all_characters:
             for variable2 in all_characters:
                if variable1 is not variable2:
                  binary_constraint = BinaryConstraint((variable1,variable2), lambda value1, value2:  value1 != value2)
                  problem.constraints.append(binary_constraint)
        
        
        #Leading digits cannot be zero              
        Leading_digits = set()
        Leading_digits.add(LHS0[0])
        Leading_digits.add(LHS1[0])
        Leading_digits.add(RHS[0])

        # make sure that the leading chars is not zero 

        for variable in all_characters:
            if variable in Leading_digits:
                problem.domains[variable] = set(range(1, 10))
            else:
                problem.domains[variable] = set(range(0, 10))
        
        # get the carrries vars and add the to list of variables
        for i in range(len(RHS)-1):
              aux.append('c'+str(i+1))
              all_characters.add('c'+str(i+1))
              problem.domains['c'+str(i+1)]=set(range(0, 2))



        
        # set the variables
        problem.variables = list(all_characters) 

        # revers the variables to process them in correct order
        LHS0= LHS0[::-1]
        LHS1=LHS1[::-1]
        RHS=RHS[::-1]
        # print('lhs0',LHS0)
        # print('lhs1',LHS1)
        # print('rhs',RHS)
        # print('lhs0',LHS0[0])
        # print('lhs1',LHS1[0])
        # print('Rhs',RHS[0])
        # print('Rhslast',RHS[len(RHS)-1])
        # print('auxlast',aux[len(aux)-1])
     
        for i in range(len(RHS)): 
            # if we are adding the first chars
            if i == 0:
            
                # concatination of the variables to make new variable
                problem.variables.append((LHS0[i],LHS1[i]))
                problem.variables.append((RHS[i],aux[i]))
                # get the domains of the new variable
                dom1=set()
                for x in problem.domains[LHS0[i]]:
                    for y in problem.domains[LHS1[i]]:
                        dom1.add((x,y))
                problem.domains[(LHS0[i],LHS1[i])] = dom1

                dom2=set()
                for x in problem.domains[RHS[i]]:
                    for y in problem.domains[aux[i]]:
                        dom2.add((x,y))
                problem.domains[(RHS[i],aux[i])] = dom2
                
                # get the constraints of the new variable
                binary_constraint = BinaryConstraint((LHS0[i],(LHS0[i],LHS1[i])), lambda x, y: x == y[0])
                problem.constraints.append(binary_constraint)

                binary_constraint = BinaryConstraint((LHS1[i],(LHS0[i],LHS1[i])), lambda x, y: x == y[1])
                problem.constraints.append(binary_constraint)

                binary_constraint = BinaryConstraint((RHS[i],(RHS[i],aux[i])), lambda x, y: x == y[0])
                problem.constraints.append(binary_constraint)

                binary_constraint = BinaryConstraint((aux[i],(RHS[i],aux[i])), lambda x, y: x == y[1])
                problem.constraints.append(binary_constraint)

                binary_constraint = BinaryConstraint(((LHS0[i],LHS1[i]),(RHS[i],aux[i])), lambda x, y: x[0] + x[1]  == y[0] + 10 * y[1])
                problem.constraints.append(binary_constraint)

            # if we are adding the last chars
            elif i == len(RHS) - 1:
                  # if the index is less than both chars len
                if i < len(LHS0) and i < len(LHS1):
                  
                    
                    problem.variables.append((LHS0[i], LHS1[i], aux[i - 1])) 

                    dom1=set()
                    for x in problem.domains[LHS0[i]]:
                        for y in problem.domains[LHS1[i]]:
                            for z in problem.domains[aux[i - 1]]:
                                    dom1.add((x,y,z))
                    problem.domains[(LHS0[i], LHS1[i], aux[i - 1])] = dom1
                    
                    binary_constraint = BinaryConstraint((LHS0[i],(LHS0[i], LHS1[i], aux[i - 1])), lambda x, y: x == y[0])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((LHS1[i],(LHS0[i], LHS1[i], aux[i - 1])), lambda x, y: x == y[1])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((aux[i-1],(LHS0[i], LHS1[i], aux[i - 1])), lambda x, y: x == y[2])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint(((LHS0[i], LHS1[i], aux[i - 1]),RHS[i]), lambda x, y: x[0] + x[1] + x[2] == y)
                    problem.constraints.append(binary_constraint)
                
                 # if the index is less than first char len and bigger than or equal the second char len
       
                elif i < len(LHS0) and i>=len(LHS1):
                  
                    
                    problem.variables.append((LHS0[i], aux[i - 1])) 

                    dom=set()
                    for x in problem.domains[LHS0[i]]:
                        for y in problem.domains[aux[i-1]]:
                                    dom.add((x,y))
                    problem.domains[(LHS0[i], aux[i - 1])] = dom
                    
                    binary_constraint = BinaryConstraint((LHS0[i],(LHS0[i], aux[i - 1])), lambda x, y: x == y[0])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((aux[i-1],(LHS0[i], aux[i - 1])), lambda x, y: x == y[1])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint(((LHS0[i], aux[i - 1]),RHS[i]), lambda x, y: x[0] + x[1] == y)
                    problem.constraints.append(binary_constraint)

                 
                # if the index is less than second char len and bigger than or equal the first char len
       
                elif i >= len(LHS0) and i<len(LHS1):
                  

                    
                    problem.variables.append((LHS1[i], aux[i - 1])) 

                    dom=set()
                    for x in problem.domains[LHS1[i]]:
                        for y in problem.domains[aux[i-1]]:
                                    dom.add((x,y))
                    problem.domains[(LHS1[i], aux[i - 1])] = dom
                    
                    binary_constraint = BinaryConstraint((LHS1[i],(LHS1[i], aux[i - 1])), lambda x, y: x == y[0])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((aux[i-1],(LHS1[i], aux[i - 1])), lambda x, y: x == y[1])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint(((LHS1[i], aux[i - 1]),RHS[i]), lambda x, y: x[0] + x[1] + x[2] == y)
                    problem.constraints.append(binary_constraint)

                  
                # if the index is grater than both chars
                elif i >= len(LHS0) and i >= len(LHS1):
                    # the last char in rhs is the last flag
                    binary_constraint = BinaryConstraint((aux[i-1],RHS[i]), lambda x, y: x == y)
                    problem.constraints.append(binary_constraint)

                    
            
            else: 
                if i < len(LHS0) and i < len(LHS1):
                   
                    
        

                    problem.variables.append((LHS0[i], LHS1[i], aux[i - 1])) 
                    problem.variables.append((RHS[i], aux[i])) 

                    dom=set()
                    for x in problem.domains[LHS0[i]]:
                        for y in problem.domains[LHS1[i]]:
                            for z in problem.domains[aux[i - 1]]:
                                dom.add((x,y,z))
                    problem.domains[(LHS0[i], LHS1[i], aux[i - 1])] = dom

                    dom=set()
                    for x in problem.domains[RHS[i]]:
                        for y in problem.domains[aux[i]]:
                            dom.add((x,y))
                    problem.domains[(RHS[i], aux[i])] = dom


                    binary_constraint = BinaryConstraint((LHS0[i],(LHS0[i], LHS1[i], aux[i - 1])), lambda x, y: x == y[0])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((LHS1[i],(LHS0[i], LHS1[i], aux[i - 1])), lambda x, y: x == y[1])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((aux[i-1],(LHS0[i], LHS1[i], aux[i - 1])), lambda x, y: x == y[2])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((RHS[i],(RHS[i], aux[i])), lambda x, y: x  == y[0])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((aux[i],(RHS[i], aux[i])), lambda x, y: x  == y[1])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint(((LHS0[i], LHS1[i], aux[i - 1]),(RHS[i], aux[i])), lambda x, y: x[0] + x[1] + x[2] == y[0] + 10 * y[1])
                    problem.constraints.append(binary_constraint)

                    


                else:
                        # if we are in the middle
                        if i < len(LHS0) and i>= len(LHS1):
                           
                    

                            problem.variables.append((LHS0[i] , aux[i - 1]))
                            problem.variables.append((RHS[i] , aux[i])) 

                            dom=set()
                            for x in problem.domains[LHS0[i]]:
                                for y in problem.domains[aux[i-1]]:
                                    dom.add((x,y))
                            problem.domains[(LHS0[i] , aux[i - 1])] = dom

                            dom=set()
                            for x in problem.domains[RHS[i]]:
                                for y in problem.domains[aux[i]]:
                                    dom.add((x,y))
                            problem.domains[(RHS[i] , aux[i])] = dom

                            binary_constraint = BinaryConstraint((LHS0[i],(LHS0[i] , aux[i - 1])), lambda x, y: x == y[0])
                            problem.constraints.append(binary_constraint)

                            #######
                            binary_constraint = BinaryConstraint((aux[i - 1],(LHS0[i] , aux[i - 1])), lambda x, y: x == y[1])
                            problem.constraints.append(binary_constraint)

                            binary_constraint = BinaryConstraint((RHS[i],(RHS[i] , aux[i])), lambda x, y: x == y[0])
                            problem.constraints.append(binary_constraint)

                            binary_constraint = BinaryConstraint((aux[i],(RHS[i] , aux[i])), lambda x, y: x == y[1])
                            problem.constraints.append(binary_constraint)

                            binary_constraint = BinaryConstraint(((LHS0[i] , aux[i - 1]),(RHS[i] , aux[i])), lambda x, y: x[0] + x[1]  == y[0] + 10 * y[1])
                            problem.constraints.append(binary_constraint)

                          

                        elif i >= len(LHS0) and i<len(LHS1):
                           
            
                
                            problem.variables.append((aux[i] , aux[i - 1]))
                            problem.variables.append((RHS[i] , aux[i])
) 

                            dom=set()
                            for x in problem.domains[LHS1[i]]:
                                for y in problem.domains[aux[i-1]]:
                                    dom.add((x,y))
                            problem.domains[(aux[i] , aux[i - 1])] = dom

                            dom=set()
                            for x in problem.domains[RHS[i]]:
                                for y in problem.domains[aux[i]]:
                                    dom.add((x,y))
                            problem.domains[ (RHS[i] , aux[i])] = dom


                            binary_constraint = BinaryConstraint((LHS1[i],(aux[i] , aux[i - 1])), lambda x, y: x == y[0])
                            problem.constraints.append(binary_constraint)   
                            
                            ################
                            
                            binary_constraint = BinaryConstraint((aux[i - 1],(LHS1[i] , aux[i - 1])), lambda x, y: x == y[1])
                            problem.constraints.append(binary_constraint)

                            binary_constraint = BinaryConstraint((RHS[i],(RHS[i] , aux[i])), lambda x, y: x == y[0])
                            problem.constraints.append(binary_constraint)

                            binary_constraint = BinaryConstraint((aux[i],(RHS[i] , aux[i])), lambda x, y: x == y[1])
                            problem.constraints.append(binary_constraint)

                            binary_constraint = BinaryConstraint(((LHS1[i] , aux[i - 1]),(RHS[i] , aux[i])), lambda x, y: x[0] + x[1]  == y[0] + 10 * y[1])
                            problem.constraints.append(binary_constraint)

   
        # print(problem.constraints)  
        return problem

    


    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())