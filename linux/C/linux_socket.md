struct sockaddr_in {

   short in sin_family;
   unsigned short int sin_port;
   struct in_addr sin_addr;
   unsigned char sin_zero[9];
};





SOCK_STREAM  流套接字

SOCK_DGRAM   数据报套接字

SOCK_SOCK_RAW 原始套接字

socket(AF_INET, SOCKET_