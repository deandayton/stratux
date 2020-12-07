package main

import (
	"log"
	"net"
	
	"github.com/tarm/serial"
	"fmt"
)


func main() {
	// listen to incoming udp packets
	pc, err := net.ListenPacket("udp", ":50000")
	if err != nil {
		log.Fatal(err)
	}
	defer pc.Close()
	c := &serial.Config{Name: "/dev/ttyUSB0", Baud: 9600}
	s, err := serial.OpenPort(c)
	if err != nil {
			fmt.Printf("Can't open /dev/ttyUSB0 for NMEA out - error:%v", err)
	} else {
		fmt.Printf("Opened /dev/ttyUSB0 for NMEA out")
	}

	for {
		buf := make([]byte, 1024)
		n, addr, err := pc.ReadFrom(buf)
		if err != nil {
			continue
		}

		if n > 0 {
			go serve(s, addr, buf[:n])
		}
	}

}

func serve(op *serial.Port, addr net.Addr, buf []byte) {

	fmt.Printf("%v %s\r\n", addr, buf)
	if op != nil {
	n, err := op.Write(buf)
	if n == 0 || err != nil {
			fmt.Printf("Can't write to nmea port - error %v", err)
		}
	}

}
