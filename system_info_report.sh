#!/bin/bash

output_file=""
if [ "$1" = "-output" ]; then
    output_file="saida.txt"  
    exec > "$output_file"   #o
fi

# Informações do sistema
echo "================= Informações do sistema ==============="
echo "SO: $(uname -o)"
echo "CPU: $(lscpu | grep 'Model name:' | cut -d: -f2)"
echo "Memória: $(free -m | grep Mem: | awk '{print $2" MB"}')"
echo "Espaço em Disco: $(df -h --total | grep total | awk '{print $2}')"
echo "Usuário: $(whoami)"
echo "Diretório Home: $HOME"

# Informações do usuário
echo "================= Informações do Usuário ==============="
echo "Diretório atual: $(pwd)"
echo "Usuários logados: $(who | awk '{print $1}' | sort | uniq)"
