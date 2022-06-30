# import modules
import winapps

softwares = []

# get each application with list_installed()
for item in winapps.list_installed():
    softwares.append(str(item.name).replace(" ","_").lower() +" "+str(item.version))
    print(str(item.name).replace(" ","_").lower() +" "+str(item.version))