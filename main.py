import sys
from random import randint
import multiprocessing 
from multiprocessing import Manager as manager
import datetime

def findValue(Dict_Pack = {}):
    lsValInt = []
    dict_val = Dict_Pack['dict_char'] 
    lsequat = Dict_Pack['ls_Equat']
    lsoperands = Dict_Pack['ls_Operand']
    res = Dict_Pack['ls_Result']
    dict_res = {}
    try:
        # print("Dict_Pack = {}".format(Dict_Pack))
        for alphaVal in lsequat:
            s=""
            for c in alphaVal:
                s += str(dict_val[c])
            # print("str : {}".format(s))
            lsValInt.append(int(s))
        # print("list Value : {}".format(lsValInt))
        s=""
        for c in res:
            s += str(dict_val[c])
        # print("str : {}".format(s))
        lsValInt.append(int(s))                

        temp = lsValInt[0]
        count = 0
        for oper in lsoperands:
            count += 1
            if oper is '+':
                temp += lsValInt[count]
            elif oper is '-' :
                temp -= lsValInt[count]
            else:
                temp += 0
                # print("out of operand")
        #     print("temp {} : {}".format(count,temp))
        # print("temp : {} = res : {}".format(temp,lsValInt[-1]))
        dict_res['Value'] = dict_val

        if not temp == lsValInt[-1]:
            # print("result not correct")
            print("Value : {}".format(dict_res['Value']))
            res_notcorrect = True
            dict_res['Result'] = False
        else :
            # print("result correct")
            print("Value : {}  - {:>15}".format(dict_res['Value'], "Correct"))
            res_notcorrect = False
            dict_res['Result'] = True
    except IOError as ioerror:
        print("Error on {}".format(ioerror))  
    else:
        return dict_res   

def main():
    eqaulSym_count = 0
    operandSym_count = 0
    alnumSym_count = 0
    notAllow_count = 0
    notAllow_char = ""
    proc = []
    lseqsub = []
    lseq = []
    lsoperand = []
    lsVal = []
    lsNumber = []
    res_notcorrect = True
    lsrand = []
    dict_char = {}
    dict_pack = {}
    dict_char_count = {}
    startnum = "0123456789"
    cpu_count = multiprocessing.cpu_count()
    pl = multiprocessing.Pool(processes = int(cpu_count))
    try:
        print("Welcome to Find for What?")
        input_equation = input("What's your Equation : ")

        for c in input_equation:
            if c is '=':
                eqaulSym_count += 1
            elif c in ['+' , '-']:
                operandSym_count += 1
            elif c.isalnum():
                alnumSym_count += 1
                dict_char[c] = 0
                if c not in dict_char_count.keys():
                    dict_char_count[c] = 1
                else :
                    dict_char_count[c] += 1
            else:
                notAllow_count += 1
                notAllow_char += c
        if not (eqaulSym_count == 1):
            raise IOError("your Equation have no \"=\"")
        elif operandSym_count == 0:
            raise IOError("your Equation have no operator [+ or -]")
        elif notAllow_count > 0:
            raise IOError("your Equation have unsupport charactor : {}".format(notAllow_char))
        elif len(input_equation) == (eqaulSym_count+operandSym_count+alnumSym_count):
            print("Status : Check passed")
            print("your Equation : {}".format(input_equation))

            eqmain , res = input_equation.split('=')
            print("Equation : {} and Result : {}".format(eqmain,res))

            if '+' not in eqmain:
                eq = eqmain.split('-')
                for eqsub in eq:
                    lsoperand.append('-')
                    lseq.append(eqsub)
                lsoperand.pop(len(lsoperand)-1)
                
            elif '-' not in eqmain:
                eq = eqmain.split('+')
                for eqsub in eq:
                    lsoperand.append('+')
                    lseq.append(eqsub)
                lsoperand.pop(len(lsoperand)-1)
            else:
                eq = eqmain.split('+')
                for eqsub in eq:
                    # print("eqsub : {}".format(eqsub))
                    if '-' in eqsub:
                        lsoperand.append('+')
                        lseqsub = eqsub.split('-')
                        for eqsubsub in lseqsub:
                            # print("eqsubsub : {}".format(eqsubsub))
                            lsoperand.append('-')
                            lseq.append(eqsubsub)  
                        lsoperand.pop(len(lsoperand)-1)
                        # print("lsoperand : {}".format(lsoperand))                   
                    else:
                        lsoperand.append('+')
                        lseq.append(eqsub)
                lsoperand.pop(0)

            len_val = len(dict_char.keys())
            offset_val = 0
            s_number = ""
            lsNumberKey = []
            lsAlphaKey = []
            for c in dict_char.keys():
                if c.isdigit():
                    # print("{} is number".format(c))
                    len_val -= 1
                    s_number += c
                    lsNumberKey.append(c)
                else:
                    lsAlphaKey.append(c)
            print("dict key length : {}".format(len_val))
            maxofnum = int(10**len_val)
            minofnum = int(startnum[:len_val])
            if s_number:
                offset_val = int(s_number)*maxofnum
            len_val = len(dict_char.keys())
            print("from : {} run to : {}".format(minofnum+offset_val,(maxofnum+offset_val)-1))
            print("list of group : {} - list operand : {} - Result : {}".format(lseq,lsoperand,res))
            print("list of Alpha : {} - list of Number : {}".format(lsAlphaKey,lsNumberKey))
            print("dict of char : {}".format(dict_char))
            print("frequency using : {}".format(dict_char_count))
            startTime = datetime.datetime.now()
            print("Start Time : {}".format(startTime.strftime("%Y-%m-%d %H:%M:%S%Z")))
            # flists = open("Numberlists.txt", 'w')
            for cnt in range(minofnum,maxofnum):
                str_cnt = "{:010d}".format(cnt)
                # print("stringofnum : {}".format(str_cnt))
                str_cnt = str_cnt[len(str_cnt)-len(lsAlphaKey):]
                goodNumber = True
                dict_letter = {}
                # print("stringofnum : {}".format(str_cnt))
                for letter in str_cnt:
                    if letter in lsNumberKey:
                        # print("False Letter : {}".format(letter))
                        goodNumber = False
                        break
                    elif letter not in dict_letter.keys():
                        dict_letter[letter] = 1
                        # print("good Letter : {}".format(dict_letter))
                    else:
                        # print("False Letter : {}".format(letter))
                        goodNumber = False
                        break
                dict_pack = {}
                if goodNumber:
                    # print("stringofnum : {}".format(str_cnt))
                    c_count = 0
                    for c in lsAlphaKey: 
                        # print("{} is not number : {}".format(c , str_cnt[c_count]))
                        dict_char[c] = int(str_cnt[c_count])
                        c_count += 1
                    for n in lsNumberKey:
                        # print("{} is number".format(n))
                        dict_char[n] = int(n)
                    # print("dict : {}".format(dict_char))
                    dict_pack['dict_char'] = dict(dict_char)
                    dict_pack['ls_Equat'] = lseq
                    dict_pack['ls_Operand'] = lsoperand
                    dict_pack['ls_Result'] = res
                    lsNumber.append(dict_pack)
                    # flists.write("Count : {} - Dict Pack Value : {}\n".format(str_cnt , dict_pack))
            # print("list of dict char : {}".format(lsNumber))
            # flists.close()
            if lsNumber:
                proc = pl.map(findValue , lsNumber)
            # print("Proc : {}".format(proc))
            flists = open("Resultlists.txt", 'w')
            flists.write("Input Equation : {}\n".format(input_equation))
            for dict_result in proc:
                # print("Result : {} - Value : {}".format(dict_result['Result'] , dict_result['Value']))
                if dict_result['Result'] == True:
                    value = dict_result['Value']
                    flists.write("Correct Value : {}\n".format(value))
                    print("Correct Value : {}".format(value))
                    s = ""
                    for c in input_equation:
                        if c in value.keys():
                            s += str(value[c])
                        else:
                            s += c
                    flists.write("Equation Value : {}\n".format(s))
                    print("Equation Value : {}".format(s))
            stopTime = datetime.datetime.now()
            diffTime = stopTime-startTime
            print("Start Time : {} - Stop Time : {}".format(startTime.strftime("%Y-%m-%d %H:%M:%S%Z") , \
                                                            stopTime.strftime("%Y-%m-%d %H:%M:%S%Z")))
            print("Use Time : {}".format(diffTime))
            flists.write("Start Time : {} - Stop Time : {}".format(startTime.strftime("%Y-%m-%d %H:%M:%S%Z") , \
                                                            stopTime.strftime("%Y-%m-%d %H:%M:%S%Z")))
            flists.write("Use Time : {}".format(diffTime))
            print("lsNumber Count : {} Proc Count : {}".format(len(lsNumber) , len(proc)))
            flists.write("Run Count : {}\n".format(len(lsNumber)))
            flists.close()

            if not lseq or not lsoperand:
                raise IOError("wrong operation on create list of operate")

    except IOError as ioerror:
        print("Error on {}".format(ioerror))   

if __name__ == "__main__":
    main()