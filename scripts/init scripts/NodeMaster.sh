#!/bin/sh /etc/rc.common

START = 50

service_start(){
  python ~/NodoCliente.py
}
