#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include <iostream> 
#include <cstdio> 
#include <cstring> 
#include <winsock2.h> 
#include "serialib.h"
#include <stdio.h>
#pragma comment(lib, "WS2_32.lib")
using namespace std;

#if defined (_WIN32) || defined(_WIN64)
	#define SERIAL_PORT "\\\\.\\COM2"
#endif
#if defined (__linux__) || defined(__APPLE__)
	#define SERIAL_PORT "/dev/ttyACM0"
#endif

serialib serial;

DWORD WINAPI serverReceive(LPVOID lpParam) { //��������� ������ �� �������
 char buffer[1024] = { 0 };
 SOCKET client = *(SOCKET*)lpParam; //����� ��� �������
 while (true) { //���� ������ �������
  if (recv(client, buffer, sizeof(buffer), 0) == SOCKET_ERROR) {
   //���� �� ������� �������� ������ ������, �������� �� ������ � �����
   cout << "recv function failed with error " << WSAGetLastError() << endl;
   return -1;
  }
  if (strcmp(buffer, "exit\n") == 0) { //���� ������ ������������
   cout << "Client Disconnected." << endl;
   break;
  }
  cout << "Client:" << buffer << endl; //����� ������� ��������� �� ������� �� ������
  serial.writeString(buffer);
  
  //memset(buffer, 0, sizeof(buffer)); //�������� �����

  //string test = serial.readString();

 }
 return 1;
}

DWORD WINAPI serverSend(LPVOID lpParam) { //�������� ������ �������
 //char buffer[1024] = { 0 };
 //SOCKET client = *(SOCKET*)lpParam;
 //while (true) {
  //fgets(buffer, 1024, stdin);
  //if (send(client, buffer, sizeof(buffer), 0) == SOCKET_ERROR) {
   //cout << "send failed with error " << WSAGetLastError() << endl;
   //return -1;
  //}
  //if (strcmp(buffer, "exit\n") == 0) {
   //cout << "Thank you for using the application" << endl;
   //break;
  //}
 //}
 return 1;
}

int main() {

	serialib serial;
	char errorOpening = serial.openDevice(SERIAL_PORT, 256000);
	
	if (errorOpening != 1) return errorOpening;
	//strw = "G0 X0 Y2 Z5"
	serial.writeString("G0 X0 Y2 Z5\r\n");

	WSADATA WSAData; //������ 
	SOCKET server, client; //������ ������� � �������
	SOCKADDR_IN serverAddr, clientAddr; //������ �������
	WSAStartup(MAKEWORD(2, 0), &WSAData);
	server = socket(AF_INET, SOCK_STREAM, 0); //������� ������
	if (server == INVALID_SOCKET) {
		cout << "Socket creation failed with error:" << WSAGetLastError() << endl;
		return -1;
	}
	serverAddr.sin_addr.s_addr = INADDR_ANY;
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(5555);

	if (bind(server, (SOCKADDR*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
		cout << "Bind function failed with error: " << WSAGetLastError() << endl;
		return -1;
	}

	if (listen(server, 0) == SOCKET_ERROR) { //���� �� ������� �������� ������
		cout << "Listen function failed with error:" << WSAGetLastError() << endl;
		return -1;
	}
	cout << "Listening for incoming connections...." << endl; 

	char buffer[1024]; //������� ����� ��� ������
	int clientAddrSize = sizeof(clientAddr); //���������������� ����� �������
	if ((client = accept(server, (SOCKADDR*)&clientAddr, &clientAddrSize)) != INVALID_SOCKET) {
	//���� ���������� �����������
		cout << "Client connected!" << endl;
		cout << "Now you can use our live chat application. " << "Enter \"exit\" to disconnect" << endl;

		DWORD tid; //�������������
		HANDLE t1 = CreateThread(NULL, 0, serverReceive, &client, 0, &tid); //�������� ������ ��� ��������� ������
		if (t1 == NULL) { //������ �������� ������
			cout << "Thread Creation Error: " << WSAGetLastError() << endl;
		}
		HANDLE t2 = CreateThread(NULL, 0, serverSend, &client, 0, &tid); //�������� ������ ��� �������� ������
			if (t2 == NULL) {
			cout << "Thread Creation Error: " << WSAGetLastError() << endl;
		}

		WaitForSingleObject(t1, INFINITE);
		WaitForSingleObject(t2, INFINITE);

		closesocket(client); //������� �����
		if (closesocket(server) == SOCKET_ERROR) {
			cout << "Close socket failed with error: " << WSAGetLastError() << endl;
			return -1;
		}
	WSACleanup();
 }
}