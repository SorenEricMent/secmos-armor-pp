sudo semanage login -a -s certadm_u -r s0:s0 certadm
sudo semanage login -a -s sysadm_u -r s0-s15:c0.c1023 sysadm
sudo semanage login -a -s secadm_u -r s0-s15:c0.c1023 secadm
