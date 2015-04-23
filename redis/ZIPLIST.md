
 ```c

#define ZIPLIST_HEAD 0
#define ZIPLIST_TAIL 1

unsigned char *ziplistNew(void);
unsigned char *ziplistPush(unsigned char *zl, unsigned char *s, unsigned int slen, int where);
unsigned char *ziplistIndex(unsigned char *zl, int index);
unsigned char *ziplistNext(unsigned char *zl, unsigned char *p);
unsigned char *ziplistPrev(unsigned char *zl, unsigned char *p);
unsigned int ziplistGet(unsigned char *p, unsigned char **sval, unsigned int *slen, long long *lval);
unsigned char *ziplistInsert(unsigned char *zl, unsigned char *p, unsigned char *s, unsigned int slen);
unsigned char *ziplistDelete(unsigned char *zl, unsigned char **p);
unsigned char *ziplistDeleteRange(unsigned char *zl, unsigned int index, unsigned int num);
unsigned int ziplistCompare(unsigned char *p, unsigned char *s, unsigned int slen);
unsigned char *ziplistFind(unsigned char *p, unsigned char *vstr, unsigned int vlen, unsigned int skip);
unsigned int ziplistLen(unsigned char *zl);
size_t ziplistBlobLen(unsigned char *zl);


```
ZIPLIST 的头 代表  0
ZIPLIST 的尾 代表  1

ZIP_END      255
ZIP_BIGEND   254

大端和小端

ZIP_STR_MASK
ZIP_INT_MASK
ZIP_int_16B
ZIP_INT_24B


ziplist> RPUSH lst 1 3 5 10086 "hello" "world"
(integer) 6

压缩列表示节约内存,

 * <zlbytes> is an unsigned integer to hold the number of bytes that the
 * ziplist occupies. This value needs to be stored to be able to resize the
 * entire structure without the need to traverse it first.
 *
 * <zltail> is the offset to the last entry in the list. This allows a pop
 * operation on the far side of the list without the need for full traversal.
 *
 * <zllen> is the number of entries.When this value is larger than 2**16-2,
 * we need to traverse the entire list to know how many items it holds.
 *
 * <zlend> is a single byte special value, equal to 255, which indicates the
 * end of the list.

<zlbytes><zltail><zllen><entry><entry><zlend>

zlen 属性值 0x4 代表4，表示压缩表有三个节点



压缩列表节点的构成



|00pppppp| - 1 byte
 *      String value with length less than or equal to 63 bytes (6 bits).
 * |01pppppp|qqqqqqqq| - 2 bytes
 *      String value with length less than or equal to 16383 bytes (14 bits).
 * |10______|qqqqqqqq|rrrrrrrr|ssssssss|tttttttt| - 5 bytes
 *      String value with length greater than or equal to 16384 bytes.
 * |11000000| - 1 byte
 *      Integer encoded as int16_t (2 bytes).
 * |11010000| - 1 byte
 *      Integer encoded as int32_t (4 bytes).
 * |11100000| - 1 byte
 *      Integer encoded as int64_t (8 bytes).
 * |11110000| - 1 byte
 *      Integer encoded as 24 bit signed (3 bytes).
 * |11111110| - 1 byte
 *      Integer encoded as 8 bit signed (1 byte).
 * |1111xxxx| - (with xxxx between 0000 and 1101) immediate 4 bit integer.
 *      Unsigned integer from 0 to 12. The encoded value is actually from
 *      1 to 13 because 0000 and 1111 can not be used, so 1 should be
 *      subtracted from the encoded 4 bit value to obtain the right value.
 * |11111111| - End of ziplist.


ZIPLIST_BYTES(zl)  获取zlbytes值

ZIPLIST_TAIL_OFFSET(zl) 获取zltail值

ZIPLIST_LENGTH(zl)

ZIPLIST_HEADER_SIZE



