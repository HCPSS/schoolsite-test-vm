# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "williamyeh/ubuntu-trusty64-docker"
  config.vm.network "private_network", ip: "192.168.33.2"

  config.vm.synced_folder "./", "/vagrant", :nfs => true

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.customize ["modifyvm", :id, "--cpus", 8]
  end

  config.ssh.forward_agent = true
  config.vm.provision "ansible" do |ansible|
    ansible.playbook  = "ansible/provision.yml"
  end
end
