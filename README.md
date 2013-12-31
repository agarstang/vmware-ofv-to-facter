vmware-ofv-to-facter
====================

External Fact that collects VMWare OVF properties using VMWare tools.

This will collect the OVF property section using VMWare tools everytime facter is run.

I have noticed occasions where VMWare stops serving the XML data so I tend to cache these as described here:
https://projects.puppetlabs.com/projects/facter/wiki/CachingExternalFacts
