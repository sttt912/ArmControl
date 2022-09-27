#include "tcpserver.h"
#include <iostream>
#include <QDebug>
#include <QSerialPortInfo>

TCPServer::TCPServer()
{
    qDebug()<<"List of available COMs:";

    Q_FOREACH(QSerialPortInfo port, QSerialPortInfo::availablePorts()){
            qDebug()<<port.portName();
    }

    qDebug()<<"Write + next to the desired port";
    qDebug()<<"Write - next to a port that is not in use";

    Q_FOREACH(QSerialPortInfo port, QSerialPortInfo::availablePorts()){
            char acc;
            qDebug()<<port.portName();
            std::cin>>acc;
            if(acc =='+'){
                comPorts.push_back(port.portName());
            }
    }
    qDebug()<<"List active porst:";
    qDebug()<<comPorts;
}

TCPServer::TCPServer(int port)
{
    this->port = port;
    Q_FOREACH(QSerialPortInfo port, QSerialPortInfo::availablePorts()){
       comPorts.push_back(port.portName());
    }
    qDebug()<<"List of all porst:";
    qDebug()<<comPorts;
}

TCPServer::~TCPServer(){
    for(int i = 0; i < Arduinos.size(); ++i){
        qDebug()<<"Closing: "<<i;
        Arduinos[i]->close();
    }
    this->close();
}


void TCPServer::startServer(){
    if(this->listen(QHostAddress::Any, port)){
        qDebug()<<"Server started";
    }
    else{
        qDebug()<<"Error\n";
    }


    qDebug()<<"Opening COM ports:";

    for(const auto &port : qAsConst(comPorts)){
        qDebug()<<"COM: "<<port;
        openComPort(port);
    }

    qDebug()<<"DONE";
    qDebug()<<"Additional information:";

    for(int i = 0; i < Arduinos.size(); ++i){
        qDebug()<<Arduinos[i];
    }

}

void TCPServer::sendComData(QString Data, QSerialPort *Com)
{
    if(!Com->isOpen()){
        qDebug()<<"COM: "<<Com;
        qDebug()<<"Error";
        return;
    }

    Data = Data + "\r";
    if (Data == "M114\r"){
        Com->write(Data.toStdString().c_str());
        qDebug()<<"COM: "<<Com;
        qDebug()<<"Data: "<<Data.toStdString().c_str();
        qDebug()<<"-------------------------------------------";
        QByteArray data = Com->readAll();
        qDebug() << "UART:" << data;
        socket->write(data);
     }else if (Data == "M119\r"){
        Com->write(Data.toStdString().c_str());
        qDebug()<<"COM: "<<Com;
        qDebug()<<"Data: "<<Data.toStdString().c_str();
        qDebug()<<"-------------------------------------------";
        QByteArray data = Com->readAll();
        qDebug() << "UART:" << data;
        socket->write(data);
     }else{
        Com->write(Data.toStdString().c_str());
        qDebug()<<"COM: "<<Com;
        qDebug()<<"Data: "<<Data.toStdString().c_str();
        qDebug()<<"-------------------------------------------";
    }

}

//Create a new comport poiter and setting up the comport(special for Arduino Uno),
//push pointer to vector(list)
void TCPServer::openComPort(QString port)
{
    qDebug()<<"Configured new COM...";
    arduino = new QSerialPort(this);
    arduino->setPortName(port);
    arduino->setBaudRate(250000);

    arduino->setDataBits(QSerialPort::Data8);
    arduino->setParity(QSerialPort::NoParity);
    arduino->setStopBits(QSerialPort::OneStop);
    arduino->setFlowControl(QSerialPort::NoFlowControl);
    //arduino->open(QSerialPort::WriteOnly);
    //arduino->open(QIODevice::WriteOnly);
    arduino->open(QIODevice::ReadWrite);
    qDebug()<<arduino->isOpen();
    Arduinos.push_back(arduino);

    qDebug()<<"DONE";

}

//Calls when new client connected successfully
void TCPServer::incomingConnection(qintptr handle){
    socket = new QTcpSocket(this);
    socket->setSocketDescriptor(handle);
    connect(socket,SIGNAL(readyRead()),this,SLOT(socketReady()));
    connect(socket,SIGNAL(disconnected()),this,SLOT(socketDisconnected()));
    qDebug()<<"New client connected! ID: "<<handle;
    //socket->write("Success connection");
}
//Read data that cames from client and pars
void TCPServer::socketReady(){
   Data = socket->readAll();
   qDebug()<<QString(Data);
   QStringList list = QString(Data).split("|");

       qDebug()<<"INCOMMING DATA";
       qDebug()<<list;

       int ARD_SIZE = Arduinos.size();

       //todo: add paralel IF it's needed...
       for(int i = 0; i < list.size();++i){
            if(i>=ARD_SIZE)
            {
                sendComData(list[i],Arduinos[i%ARD_SIZE]);
            }
            else
            {
                sendComData(list[i],Arduinos[i]);
            }
       }
}
//call after client disconnected and delete socket
void TCPServer::socketDisconnected(){
    socket->deleteLater();

}
