  #!/bin/bash
case    $1    in
start)

echo  "Iniciando..."
echo -n " Limpando as tabelas... "
                iptables -F INPUT
                iptables -F OUTPUT
                iptables -F FORWARD
                iptables -t nat -F POSTROUTING
                iptables -t nat -F PREROUTING
echo "Ok"

echo -n "Bloqueando tudo nas tabelas INPUT, OUTPUT e FORWARD... "
               iptables -P INPUT DROP
               iptables -P OUTPUT DROP
               iptables -P FORWARD DROP
echo "Ok"

echo -n "Liberando a interface de loopback... "
               iptables -A INPUT -i lo -j ACCEPT
               iptables -A OUTPUT -o lo -j ACCEPT
echo "OK"

echo -n "Aceita o ping... "
   iptables -A INPUT -i eth0 -p icmp -m limit --limit 2/s -j ACCEPT
echo "OK"

echo -n "Fornecer as conexões estabelecidas e relacionadas... "
   iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
echo "OK"

echo -n "Permitir todas as conexões validas de saida... "
 iptables -A OUTPUT -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
echo "OK"

echo -n "Liberando portas BIND9 e SSH... "
             PORTAS="53 22"
             for   i   in $PORTAS;do
             iptables -I INPUT -p tcp --dport $i -j ACCEPT
             iptables -I OUTPUT -p tcp --sport $i -j ACCEPT
done
echo "Ok"

echo -n "Mascarando a rede usando o NAT... "
echo 1 > /proc/sys/net/ipv4/ip_forward           
         iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -o eth0 -j MASQUERADE
         iptables -I FORWARD -s 192.168.0.0/24 -i eth1 -o eth0 -j ACCEPT
         iptables -I FORWARD -d 192.168.0.0/24 -o eth1 -i eth0 -j ACCEPT
echo "Ok"
;;
stop)
echo -n "Limpando as Regras... "
            iptables -F INPUT
            iptables -F OUTPUT
            iptables -F FORWARD
            iptables -t nat -F POSTROUTING
            iptables -t nat -F PREROUTING
echo "Ok"

echo -n "Aceitando tudo nas tabelas... "
            iptables -P INPUT ACCEPT
            iptables -P OUTPUT ACCEPT
            iptables -P FORWARD ACCEPT
echo "Ok"
;;
esac
