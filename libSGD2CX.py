# *****************************************************
#  Script:       libSGD2CX.py
#  Description:  Create a Cerberus X module for libSGD
#  Author:       Michael Hartlef
#  Version:      1.03
#  License:      MIT
#  Copyright:    (c) 2024 Michael Hartlef
# *****************************************************

import os
import sys
import subprocess

# Change type from C++ to CerberusX
def ChangeType(typename):
    ret = ""
    if typename=="void":
        ret = "Void"
    elif typename=="void*":
        ret = "Int"
    elif typename=="int":
        ret = "Int"
    elif typename=="bool":
        ret = "Bool"
    elif typename=="float":
        ret = "Float"

    elif typename=="SGD_Bool":
        ret = "Int"
    elif typename=="SGD_Real":
        ret = "Float"
    elif typename=="SGD_String":
        ret = "String"
    elif typename=="SGD_Sound":
        ret = "Int"
    elif typename=="SGD_Surface":
        ret = "Int"
    elif typename=="SGD_Texture":
        ret = "Int"
    elif typename=="SGD_Light":
        ret = "Int"
    elif typename=="SGD_Entity":
        ret = "Int"
    elif typename=="SGD_Material":
        ret = "Int"
    elif typename=="SGD_Mesh":
        ret = "Int"
    elif typename=="SGD_Model":
        ret = "Int"
    elif typename=="SGD_Sprite":
        ret = "Int"
    elif typename=="SGD_Skybox":
        ret = "Int"
    elif typename=="SGD_Camera":
        ret = "Int"
    elif typename=="SGD_Font":
        ret = "Int"
    elif typename=="SGD_Image":
        ret = "Int"
    elif typename=="SGD_Collider":
        ret = "Int"
    else:
        ret = ""
    return ret

# Change type from CerberusX to C++
def ChangeType2(typename):
    ret = ""
    if typename=="void":
        ret = "void"
    elif typename=="void*":
        ret = "int"
    elif typename=="int":
        ret = "int"
    elif typename=="bool":
        ret = "bool"
    elif typename=="float":
        ret = "float"

    elif typename=="SGD_Bool":
        ret = "int"
    elif typename=="SGD_Real":
        ret = "double"
    elif typename=="SGD_String":
        ret = "String"

    elif typename=="SGD_Sound":
        ret = "int"
    elif typename=="SGD_Surface":
        ret = "int"
    elif typename=="SGD_Texture":
        ret = "int"
    elif typename=="SGD_Light":
        ret = "int"
    elif typename=="SGD_Entity":
        ret = "int"
    elif typename=="SGD_Material":
        ret = "int"
    elif typename=="SGD_Mesh":
        ret = "int"
    elif typename=="SGD_Model":
        ret = "int"
    elif typename=="SGD_Sprite":
        ret = "int"
    elif typename=="SGD_Skybox":
        ret = "int"
    elif typename=="SGD_Camera":
        ret = "int"
    elif typename=="SGD_Font":
        ret = "int"
    elif typename=="SGD_Image":
        ret = "int"
    elif typename=="SGD_Collider":
        ret = "int"
    else:
        ret = ""
    return ret

def install(module):
    subprocess.check_call(['pip', 'install', module])
    print(f"The module {module} was installed")

if __name__ == '__main__':
        
    # Check if shutil is available and if not, install it.
    try:
        import shutil
    except ModuleNotFoundError:
        install('shutil')

    # Check if argparse is available and if not, install it.
    try:
        import argparse
    except ModuleNotFoundError:
        install('argparse')



    librarypath  = os.path.realpath("./lib")
    includepath  = os.path.realpath("./include/sgd")
    cerberuspath = os.path.realpath("./cerberus/modules_ext/libSGD")

    parser = argparse.ArgumentParser(prog='libSGD2CX') #, allow_abbrev=False)
    parser.add_argument('-l','--library',  help="Path to the lib files")
    parser.add_argument('-i','--include',  help="Path to the header files")
    parser.add_argument('-c','--cerberus', help="Path to the Cerberus X module directory")
    parser.add_argument('-v','--verbose',  help="no output of messages", action="store_true")

    args = parser.parse_args()

    if args.library:
        librarypath = os.path.realpath(args.library)
    if args.include:
        includepath = os.path.realpath(args.include)
    if args.cerberus:
        cerberuspath = os.path.realpath(args.cerberus)
    if not (os.path.isdir(librarypath)):
        print ("LibraryPath ",librarypath," doesn't exist!")
        sys.exit(2)
    if not (os.path.isdir(includepath)):
        print ("IncludePath ",includepath,"doesn't exist!")
        sys.exit(2)

    # Remove existing export directories and its content
    if (os.path.isdir(cerberuspath)):
        if not args.verbose:
            print ('Removing a Cerberus X module at',cerberuspath)
        shutil.rmtree(cerberuspath, ignore_errors=False, onerror=None)

    # Create export directories
    if not os.path.isdir(cerberuspath+"/native/lib"):
        if not args.verbose:
            print ("Creating directory at",cerberuspath+"/native/lib")
        try:  
            os.makedirs(cerberuspath+"/native/lib")  
        except OSError as error:  
            print(error) 

    if not os.path.isdir(cerberuspath+"/cerberusdoc"):
        if not args.verbose:
            print ("Creating directory at",cerberuspath+"/cerberusdoc")
        try:  
            os.makedirs(cerberuspath+"/cerberusdoc")  
        except OSError as error:  
            print(error) 

    # Copy library files
    if not args.verbose:
        print ("Copy libraries from",librarypath, "to",cerberuspath+"/native/lib directory...")
    shutil.copy2(librarypath+"/sgd_dynamic.dll",cerberuspath+"/native/lib/sgd_dynamic.dll")
    shutil.copy2(librarypath+"/sgd_dynamic.lib",cerberuspath+"/native/lib/sgd_dynamic.lib")

    # Copy the header files
    if not args.verbose:
        print ("Copy header files from",includepath,"to",cerberuspath+"/native directory...")
    shutil.copy2(includepath+"/sgd.h",cerberuspath+"/native/sgd.h")
    shutil.copy2(includepath+"/keycodes.h",cerberuspath+"/native/keycodes.h")

    # correct sgd header file from API definitions over more than one line and SGD_REAL allways to be a double
    if not args.verbose:
        print ("Correcting",cerberuspath+"/native/sgd.h...")
    newsgd = ""
    tmpline = ""
    file = open(cerberuspath+"/native/sgd.h", "r", encoding="utf8")
    lines = file.readlines()
    for line in lines:
        if line.startswith("typedef float SGD_Real;"):
            line = line.replace("typedef float SGD_Real;", "typedef double SGD_Real;     //typedef float SGD_Real;     // correction for Cerberus X")
        if len(tmpline)>=3:
            line = tmpline + line.strip() + "\n"
            tmpline = ""
        if line.startswith("SGD_API ") and line.endswith(",\n"):
            tmpline = line.replace('\n', '').replace('\r', '')
            continue
        newsgd = newsgd + line
    file.close()

    # create the Cerberus X doc file 
    with open(cerberuspath+"/native/sgd.h", 'w', encoding="utf8") as f:
        f.write(newsgd)
        f.close()
    if not args.verbose:
        print ("Correcting",cerberuspath+"/native/sgd.h done!")


    # convert keycodes header file
    if not args.verbose:
        print ("Converting",cerberuspath+"/native/keycodes.h","start...")
    newcontent = ""
    lfound = 0
    file = open(cerberuspath+"/native/keycodes.h", "r", encoding="utf8")
    lines = file.readlines()
    for line in lines:
        if line.startswith("#ifndef"):
            line = line.replace("#ifndef", "' ifndef")
        if line.startswith("#endif"):
            line = line.replace("#endif", "' endif")
        if line.startswith("#define SGD_KEYCODES_H_INCLUDED"):
            line = line.replace("#define SGD_KEYCODES_H_INCLUDED", "' define SGD_KEYCODES_H_INCLUDED")
    
        if line.startswith("//"):
            line = line.replace("//", "' ")
        if line.startswith("/*"):
            line = line.replace("/*", "' ")
        if line.startswith("#define "):
            llist = line.split(" ")
            line = "Const "+ llist[1] + ":Int = " + llist[2]
            line = line.replace("= 0x","= x")

        if not (line .startswith("'") or len(line)<5):
            newcontent = newcontent + line

    file.close()
    with open(cerberuspath+"/keycodes.cxs", 'w', encoding="utf8") as f:
        f.write(newcontent)
    if not args.verbose:
        print ("Converting",cerberuspath+"/native/keycodes.h","done!")



    # convert sgd header file
    if not args.verbose:
        print ("Converting",cerberuspath+"/native/sgd.h","start...")

    newcontent = ""
    speciallines = ""
    cpplines = ""
    newconst = ""
    doclines = ""
    doclines2 = ""
    namespace = "libsgd"
    docmodules = {}
    namespaces = {}
    namespacesc = {}
    namespacescc = {}

    lfound = 0
    file = open(cerberuspath+"/native/sgd.h", "r", encoding="utf8")
    lines = file.readlines()
    for line in lines:
        if line.startswith("#define SGD_API"):
            line = line.replace("#define SGD_API", "' define SGD_API")
        if line.startswith("#define SGD_EXTERN"):
            line = line.replace("#define SGD_EXTERN", "' define SGD_EXTERN")
        if line.startswith("#define SGD_DECL"):
            line = line.replace("#define SGD_DECL", "' define SGD_DECL")
        if line.startswith("#elif"):
            line = line.replace("#elif", "' elif")
        if line.startswith("typedef"):
            line = line.replace("typedef", "' typedef")
        if line.startswith("#if "):
            line = line.replace("#if ", "' if ")
        if line.startswith("#else"):
            line = line.replace("#else", "' else")
        if line.startswith("#include "):
            line = line.replace("#include ", "' include ")
        if line.startswith("#ifndef "):
            line = line.replace("#ifndef ", "' ifndef ")
        if line.startswith("#endif"):
            line = line.replace("#endif", "' endif")
        if line.startswith("#define SGD_SGD_H_INCLUDED"):
            line = line.replace("#define SGD_SGD_H_INCLUDED", "' define SGD_SGD_H_INCLUDED")

        if line.startswith("//! @name ") and line.find('Typedefs')<=0 and line.find('ImGui')<=0:
            lp = line.find('@name')
            namespace = line[lp+6:].replace('\n', '').replace('\r', '')
            namespace = namespace.replace(' ','_').lower()
            namespace = namespace.replace('2d_overlay','overlay2D').lower()
            line = 'Module libSGD.'+namespace+'\n\n'
            namespaces.update({namespace:"# Module."+namespace})
            namespacesc.update({namespace:"\n"})
            namespacescc.update({namespace:"' "+namespace+'.cxs\n'})
             
        elif line.startswith("//"):
            line = line.replace("//", "' ")
        elif line.startswith("/*"):
            line = line.replace("/*", "' ")

        if line.find("sgd_SetErrorHandler")>1:
            line = "' " + line
        elif line.find("sgd_ImGui_ImplSGD")>1:
            line = "' " + line
        elif line.startswith("' !") and not line.startswith("' ! @") and not line.find("Quick links: sgd.h keycodes.h")>-1 and not line.find("LibSGD reference doc")>-1:
            ls = len(line)-4
            if not line[-ls:].startswith("' !"):
                doclines2 = doclines2 + line[-ls:] + "\n"
        elif line.startswith("SGD_API "):
            line = line.replace(");", ")")
            line = line.replace("SGD_API ", "")
            line = line.replace("SGD_DECL ", "")
            llist = line.split("(")
            llist[1] = llist[1].replace(")","")
            llist[1] = llist[1].replace(", ",",")
            functions = llist[0].split(" ")
            params = llist[1].split(",")

            nl = "Function " + functions[1]+":"+ChangeType(functions[0])+" ("
            nl2 = ChangeType2(functions[0])+" _"+functions[1]+"("
            if len(llist[1])>1:
                p1 = 0
                #print (line)
                for param in params:
                    p1 = p1 + 1
                    if p1 >1:
                        nl = nl +", "
                        nl2 = nl2 +", "
                    pars = param.split(" ")    
                    nl = nl +pars[1].replace('\n', '').replace('\r', '').replace('property','propert')+":"+ChangeType(pars[0])
                    nl2 = nl2 +ChangeType2(pars[0])+" "+pars[1].replace('\n', '').replace('\r', '').replace('property','propert')
            nl = nl +")"
            nl2 = nl2 +") {\n\t"
            if ChangeType2(functions[0])!="void":
                nl2 = nl2 + 'return '
            nl2 = nl2 + functions[1]+"("

            if len(llist[1])>1:
                p1 = 0
                for param in params:
                    p1 = p1 + 1
                    if p1 >1:
                        nl2 = nl2 +", "
                    pars = param.split(" ")    
                    nl2 = nl2 +pars[1].replace('\n', '').replace('\r', '').replace('property','propert')
                    if ChangeType2(pars[0])=="String":
                        nl2 = nl2 + '.ToCString<char>()'
            nl2 = nl2 +');'

            nl2 = nl2 +"\n}\n"
            if nl.find("String")>5 or ChangeType2(functions[0])=="String":
                nl = nl + " = "+'"_'+functions[1]+'"'
                cpplines = cpplines + nl2 + "\n"
            line = nl+"\n"

        if line.startswith("#define "):
            line = " ".join(line.split())
            llistc = line.split(" ")
            line = "Const "+ llistc[1] + ":Int = " + llistc[2]+"\n"
            line = line.replace("= 0x","= x")
            if line.endswith("f\n"):
                line = line.replace("f","")
                line = line.replace(":Int",":Float")
                line = line.replace("= .","= 0.")

        
        if not (line .startswith("'") or len(line)<5):
            tmpdoc = ""
            tmpsrc = ""
            if line.startswith("Function"):
                if line.find(' = "_sgd_')>3:
                    speciallines = speciallines + '\t' + line
                    lp = line.find(' = "_sgd_')
                    doclines = doclines + "# " + line[0:lp]+"\n\n"
                    doclines = doclines + doclines2+"\n"
                    if namespace in namespacesc:
                        tmpsrc = namespacesc.get(namespace)
                        tmpsrc = tmpsrc + '\t' + line[0:lp] +"\n"
                    else:
                        tmpsrc = '\t' + line +"\n"
                    namespacesc.update({namespace:tmpsrc}) 
                    
                    if namespace in namespaces:
                        tmpdoc = namespaces.get(namespace)
                        tmpdoc = tmpdoc + "# " + line[0:lp] +"\n\n"+ doclines2
                    else:
                        tmpdoc = "# " + line +"\n"
                    namespaces.update({namespace:tmpdoc}) 
                    
                    doclines2 = ""
                    #print (namespace+"->"+line[0:lp])
                else:       
                    newcontent = newcontent + '\t' + line
                    doclines = doclines + "# " + line +"\n"
                    doclines = doclines + doclines2+"\n"

                    if namespace in namespaces:
                        tmpsrc = namespacesc.get(namespace)
                        tmpsrc = tmpsrc + '\t' + line #+"\n"
                    else:
                        tmpsrc = '\t' + line #+"\n"
                    namespacesc.update({namespace:tmpsrc}) 

                    if namespace in namespaces:
                        tmpdoc = namespaces.get(namespace)
                        tmpdoc = tmpdoc + "# " + line +"\n"+ doclines2
                    else:
                        tmpdoc = "# " + line +"\n"
                    namespaces.update({namespace:tmpdoc}) 
                    doclines2 = ""

            elif line.startswith("Module"):
                doclines = doclines + "# " + line +"\n"
                docline2 = ""
                namespaces.update({namespace:'\n# Module libSGD.'+namespace+'\n\n'}) 
                #namespacesc.update({namespace:"' "+'Module libSGD.'+namespace+'\n\n'}) 
                         
            else:
                newconst = newconst + line
                doclines = doclines + "# " + line +"\n"
                docline2 = ""

                if namespace in namespacescc:
                    tmpsrc = namespacescc.get(namespace)
                    tmpsrc = tmpsrc + line #+"\n"
                else:
                    tmpsrc = line #+"\n"          
                namespacescc.update({namespace:tmpsrc})          


                if namespace in namespaces:
                    tmpdoc = namespaces.get(namespace)
                    tmpdoc = tmpdoc + "# " + line +"\n"
                else:
                    tmpdoc = "# " + line +"\n"          
                namespaces.update({namespace:tmpdoc})          

    file.close()

    # create the Cerberus X module
    with open(cerberuspath+"/libSGD.cxs", 'w', encoding="utf8") as f:
        f.write('#If TARGET<>"stdcpp"\n')
        f.write('#Error "Use the C++ Tool target to build your game!"\n')
        f.write("#Endif\n")
        f.write("\n")
        f.write('#CC_OPTS += "-DSGD_DYNAMIC=1"\n')
        f.write('#CC_LDOPTS+="-L../"\n')
        f.write('#CC_LIBS += "-lsgd_dynamic"\n')
        f.write("\n")
        f.write('Include "native\lib\sgd_dynamic.dll"\n')
        f.write('Include "native\lib\sgd_dynamic.lib"\n')
        f.write('Include "native\keycodes.h"\n')
        f.write('Include "native\sgd.h"\n')
        f.write('Import "native\sgd.cpp"\n')
        f.write("\n")
        f.write("Import keycodes\n\n")
        for nk in namespacesc.keys():
            if nk != 'libsgd':
                f.write('Import '+nk+'\n')
        f.write('\n')
        #f.write(newconst)
        if "libsgd" in namespacescc:
            f.write(namespacescc.get("libsgd")+'\n')
        #f.write(newcontent)
        #f.write("\n\n")
        #f.write(speciallines)
        if "libsgd" in namespacesc:
            f.write("Extern\n\n")
            f.write(namespacesc.get("libsgd")+'\n')
        f.close()

    for nk, nv in namespaces.items():
        if nk != 'libsgd':
            #print (nv)
            with open(cerberuspath+"/"+nk+".cxs", 'w', encoding="utf8") as f:
                #f.write(nv)
                if nk in namespacescc:
                    f.write(namespacescc.get(nk))
                if nk in namespacesc:
                    f.write("\nExtern\n")
                    f.write(namespacesc.get(nk))
                f.close()




    # create the Cerberus X cpp file to store the special functions with string conversion and including the header file
    with open(cerberuspath+"/native/sgd.cpp", 'w', encoding="utf8") as f:
        f.write('#include "sgd.h"\n\n')
        f.write(cpplines)
        f.close()

    # create the Cerberus X doc file 
    with open(cerberuspath+"/cerberusdoc/libSGD.cerberusdoc", 'w', encoding="utf8") as f:
        f.write('# Module libSGD\n\n')
        for nk in namespaces.keys():
            if nk != 'libsgd':
                f.write('# Import libSGD.'+nk+'\n\n')
        f.write('\n')
        f.write('LibSGD reference documentation\n\n')
        f.write('It is a simple game development library, created by Mark Sibly, that provides a high level, easy to use *scene graph* style API for writing games and apps.\n\n')
        f.write('The module also support loading and playing audio and will eventually include network functionality.\n\n')
        f.write('You can find the support forum at [[https://skirmish-dev.net/forum]]\n\n')
        f.write('The GitHub repository is located at [[https://github.com/blitz-research/libsgd]]\n\n')
        f.write('If you want to support LibSGD, you can do so at [[https://patreon.com/libsgd]]\n\n')
        f.write('Attention: The module current only works on Windows and is build via the *C++ Tool* target\n\n')
        f.write('<pre>Strict\n')
        f.write('Import libSGD\n\n')
        f.write('Function Main:Int()\n\n')
        f.write('    sgd_Init()\n')
        f.write('    sgd_CreateWindow(640, 480, "Hello from Cerberus X", 0)\n')
        f.write('    sgd_CreateScene()\n')
        f.write('    sgd_SetSceneClearColor(.5,.2,0,1)\n\n')
        f.write('    While((sgd_PollEvents() & SGD_EVENT_MASK_CLOSE_CLICKED)=0)\n')
        f.write('        sgd_RenderScene()\n')
        f.write('        sgd_Present()\n')
        f.write('        sgd_Clear2D()\n')
        f.write('        sgd_Draw2DText(sgd_FPS(),10,10)\n')
        f.write('    Wend\n\n')
        f.write('    sgd_Terminate()\n\n')
        f.write('    Return 0\n')
        f.write('End\n')
        f.write('</pre>\n\n')
        #f.write(doclines)
        f.write(namespaces.get("libsgd")+'\n')
        f.close()

    for nk, nv in namespaces.items():
        if nk != 'libsgd':
            #print (nv)
            with open(cerberuspath+"/cerberusdoc/"+nk+".cerberusdoc", 'w', encoding="utf8") as f:
                f.write(nv)
                f.close()

    if not args.verbose:
        print ("Converting",cerberuspath+"/native/sgd.h","done!")

