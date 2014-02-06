#!/usr/bin/python

#stdlib
import json
import os
import subprocess
from xml.dom.minidom import parseString


def which(cmd):
    """Python implementation of `which` command."""
    for path in os.environ["PATH"].split(os.pathsep):
        file = os.path.join(path, cmd)
        if os.path.exists(file) and os.access(file, os.X_OK):
            return file
        elif os.name == "nt":
            for ext in os.environ["PATHEXT"].split(os.pathsep):
                full = file + ext
                if os.path.exists(full) and os.access(full, os.X_OK):
                    return full
    return None


FACTER = which("facter")
VMTOOLS = which("vmtoolsd")


def facter(*args):
    facts = json.loads(
        subprocess.check_output([FACTER, '--json', '--no-external'] +
                                [arg for arg in args])
    )
    return facts


def findXmlSection(dom, sectionName):
    sections = dom.getElementsByTagName(sectionName)
    return sections[0]


def getOVFProperties(ovfEnv):
    dom = parseString(ovfEnv)
    section = findXmlSection(dom, "PropertySection")
    propertyMap = {}
    for property in section.getElementsByTagName("Property"):
        key = property.getAttribute("oe:key")
        value = property.getAttribute("oe:value")
        propertyMap[key] = value
    dom.unlink()
    return propertyMap


def getVMWareOvfEnv():
    if VMTOOLS is None:
        raise Exception("VMWare Tools not installed.")
    try:
        ovf = subprocess.check_output(
            [VMTOOLS, '--cmd', 'info-get guestinfo.ovfenv'],
            stderr=subprocess.STDOUT
        )
        properties = getOVFProperties(ovf)
        print "ovf=true"
        for key, value in properties.iteritems():
            print "ovf_" + key + "=" + value
    except:
        print "ovf=false"
        return


if __name__ == "__main__":
    facts = facter("is_virtual", "virtual")
    if (facts['is_virtual'] == 'true') and (facts['virtual'] == 'vmware'):
        getVMWareOvfEnv()
