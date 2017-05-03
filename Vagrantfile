# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.define "search" do |search|
    search.vm.box = "ubuntu/xenial64"
    search.vm.network "private_network", ip: "192.168.33.5"

    search.vm.provider "virtualbox" do |vb|
      vb.memory = "4096"
      vb.customize ["modifyvm", :id, "--cpus", 2]
    end

    search.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y default-jdk
      sysctl -w vm.max_map_count=262144
    SHELL

    search.vm.provision "shell", privileged: false, inline: <<-SHELL
      curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.3.0.tar.gz
      tar -xvf elasticsearch-5.3.0.tar.gz
      echo "network.host: 0.0.0.0" >> ./elasticsearch-5.3.0/config/elasticsearch.yml
      echo "http.host: 0.0.0.0" >> ./elasticsearch-5.3.0/config/elasticsearch.yml
      echo "transport.host: 127.0.0.1" >> ./elasticsearch-5.3.0/config/elasticsearch.yml
      echo "script.inline: on" >> ./elasticsearch-5.3.0/config/elasticsearch.yml

      wget https://artifacts.elastic.co/downloads/kibana/kibana-5.3.0-linux-x86_64.tar.gz
      tar -xzf kibana-5.3.0-linux-x86_64.tar.gz

      ./elasticsearch-5.3.0/bin/elasticsearch -d
      nohup ./kibana-5.3.0-linux-x86_64/bin/kibana -e http://192.168.33.5:9200 -H 192.168.33.5 > /dev/null 2>&1 &
    SHELL
  end

  config.vm.define "schools" do |schools|
    schools.vm.box = "ubuntu/xenial64"
    schools.vm.network "private_network", ip: "192.168.33.2"

    schools.vm.synced_folder "./", "/vagrant", :nfs => true

    schools.vm.provider "virtualbox" do |vb|
      vb.memory = "4096"
      vb.customize ["modifyvm", :id, "--cpus", 2]
    end

    schools.vm.provision "ansible" do |ansible|
      ansible.playbook  = "ansible/provision.yml"
    end
  end
end
