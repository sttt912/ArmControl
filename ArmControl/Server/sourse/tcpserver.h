#ifndef TCPSERVER_H
#define TCPSERVER_H

#include <QTcpServer>
#include <QTcpSocket>
#include <QObject>
#include <QSerialPort>

class TCPServer : public QTcpServer
{
    Q_OBJECT
public:
    TCPServer();
    TCPServer(int port);
    ~TCPServer();
    QByteArray Data;
private:
    QTcpSocket* socket = nullptr;
    int port = 1331;
    QSerialPort *arduino;
    static const quint16 vendor_id = 9025;
    static const quint16 product_id = 67;
    QVector<QString> comPorts;
    QVector<QSerialPort*> Arduinos;
    void openComPort(QString port);

public:
    void setPort();
    void sendComData(QString Data, QSerialPort *Com);   //Convert bytes to string to char and send to comport


public slots:
    void startServer(); //Starts TCP server
    void incomingConnection(qintptr socketDescriptor);  //Calls when new client connected successfully
    void socketReady(); //Read data that cames from client and pars
    void socketDisconnected();  //call after client disconnected and delete socket

};

#endif // TCPSERVER_H
