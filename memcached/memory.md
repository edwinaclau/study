

##一）模型分析
 在开始解剖memcached关于内存管理的源代码之前，先宏观上分析一下memcached内存管理的模型是怎样子的：

提个建议，我觉得memcached内存管理的模型与我们平时做作业的作业本“画格子给我们往格子里面写字”的逻辑很像，一本本作业本就是我们的内存空间，而我们往里写的字就是我们要存下来的数据，所以分析的时候可以想像一下用方格作业本写字的情景。

* 1）首先，先介绍memcached中关于内存管理的几个重要的概念：

* a）slab、chunk

* slab是一块内存空间，默认大小为1M，而memcached会把一个slab分割成一个个chunk，比如说1M的slab分成两个0.5M的chunk，所以说slab和chunk其实都是代表实质的内存空间，chunk只是把slab分割后的更小的单元而已。
slab就相当于作业本中的“页”，而chunk则是把一页画成一个个格子中的“格”。

* b）item

##item是我们要保存的数据，例如php代码：$memcached->set(“name”,”abc”,30);代表我们把一个key为name，value为abc的键值对保存在内存中30秒，那么上述中的”name”, “abc”, 30这些数据实质都是我们要memcached保存下来的数据， memcached会把这些数据打包成一个item，这个item其实是memcached中的一个结构体（当然结构远不止上面提到的三个字段这么简单），把打包好的item保存起来，完成工作。而item保存在哪里？其实就是上面提到的”chunk”，一个item保存在一个chunk中。

##chunk是实质的内存空间，item是要保存的东西，所以关系是：item是往chunk中塞的。

##还是拿作业本来比喻，item就是相当于我们要写的“字”，把它写到作业本某一“页（slab）”中的“格子（chunk）”里。

* c）slabclass

通过上面a）b）我们知道，slab（都假设为1M）会割成一个个chunk，而item往chunk中塞。

那么问题来了：

我们要把这个1M的slab割成多少个chunk？就是一页纸，要画多少个格子？

我们往chunk中塞item的时候，item总不可能会与chunk的大小完全匹配吧，chunk太小塞不下或者chunk太大浪费了怎么办？就是我们写字的时候，格子太小，字出界了，或者我们的字很小写在一个大格子里面好浪费。

所以memcached的设计是，我们会准备“几种slab”，而不同一种的slab分割的chunk的大小不一样，也就是说根据“slab分割的chunk的大小不一样”来分成“不同的种类的slab”，而 slabclass就是“slab的种类”的意思了。

继续拿作业本来比喻：假设我们现在有很多张A4纸，有些我们画成100个格子，有些我们画成200个格子，有些300…。我们把画了相同个格子（也相同大小）的纸钉在一起，成为一本本“作业本”，每本“作业本”的格子大小都是一样的，不同的“作业本”也代表着“画了不同的大小格子的A4纸的集合”，而这个作业本就是slabclass啦！

所以当你要写字（item）的时候，你估一下你的字有多“大”，然后挑一本作业本（slabclass），在某一页（slab）空白的格子（chunk）上写。（我真是学霸。。-_-||）

每个slabclass在memcached中都表现为一个结构体，里面会有个指针，指向它的那一堆slab。

2）对上面的概念有了个感性的认识了，我们来解剖memcached中比较重要的结构体和变量：

a）slabclass_t（即上面说到的slabclass类型）
1.typedef struct {
2.    unsigned int size;  //chunk的大小 或者说item的大小
3.    unsigned int perslab;//每个slab有多少个item，slab又称“页”
4.    /**
5.    下面这个slots的解析：
6.    当前slabclass的空闲item链表，也是可用item链表，当前slabclass一切可以用的内存空间都在此，
7.    这里是内存分配的入口，分配内存的时候都是在这个链表上挤一个出去。
8.    ps：memcached的新版本才开始把slots作为“所有空闲的item链接”的用途，以前的版本slots链表保存的是“回收的item”的意思，
9.    而旧版本新分配的slab，是用end_page_ptr指针及end_page_free来控制，此版本已不用。
10.    */
11.    void *slots;
12.    unsigned int sl_curr; //当前slabclass还剩多少空闲的item，即上面的slots数
13.    unsigned int slabs;  //这个slabclass分配了多少个slab了
14.    /**
15.    下面slab_list和lisa_size的解析：
16.    slab_list是这个slabclass下的slabs列表，逻辑上是一个数组，每个元素是一个slab指针。
17.    list_size是slab_list的元素个数。
18.    注意这个list_size和上面的slabs的不同：
19.        由于slab_list是一个空间大小固定的数组，是数组！而list_size是这个数组元素的个数，代表slab_list的空间大小。
20.        slabs代表已经分配出去的slabs数，list_size则代表可以有多少个slabs数
21.        所以当slabs等于list_size的时候代表这个slab_list已经满了，得增大空间。
22.    */
23.    void **slab_list;
24.    unsigned int list_size;
25.    unsigned int killing; /* index+1 of dying slab, or zero if none */
26.    size_t requested; /* The number of requested bytes */
27.} slabclass_t;


代码注释中已经把大部分字段解析了，但再重点解析一个字段：slot，很重要。

回想我们的作业本，写字的时候只需要知道作业本中的下一个空白格子在哪里然后写上去即可，因为用作业本写字是有规律的，总是从第一页第一行左边开始往右写，所以已经用的格子总是连续的。

旧版本的memcached也是用这种思路，每个slabclass保存着一个指向下一个空白chunk的指针的变量（end_page_ptr），但memcached内存管理和写作业很不一样的地方在于，memcached里面保存的item是会过期的，而且每个item的过期时间都很可能不一样，也就是说作业本里面有些字会过期，过期之后相应的空格可以回收并再次利用，由于这些回收的item是不连续的，所以旧版本的memcached把每个slabclass中过期的item串成一个链表，而每个slabclass中的slot就是它相应的被回收的item链表。所以旧版本的memcached在分配内存空间的时候，先去slot找有没有回收的item，没有的话再去end_page_ptr找到下一个新的可用的空白的chunk。

新版本的memcached包括现在分析的1.4.20版本，memcached把旧版本end_page_ptr去掉，把新的可用的chunk也整合到slot中，也就是说slot的定义由“回收的item”变为“空闲可用的item”，每当我们新开辟一个slab并把它分割成一个个chunk的时候，同时马上把这些chunk先初始化成有结构的item（item是一个结构体），只是这个item的用户数据字段为空，待填充状态，称这些item为”free的item”，并把这些free的item串成链表保存在slot中。而旧的item过期了，回收了，也变成”free的item”，也同样插入到这个slot链表中。所以在新版本memcached中slabclass的slot的概念是指“空闲的item链表”！虽然这时内存分配的逻辑没有旧版本那样像作业本的思路那么形象，但代码和逻辑都变得更纯粹了，每次要分配内存，只需要直接从slot链表中拿一个出去即可。

memcached在启动的时候会实例化几本“作业本”：
1.static slabclass_t slabclass[MAX_NUMBER_OF_SLAB_CLASSES];


slabclass[i]就是一本”作业本”，i理解为作业本的id。

b）item结构体
1.typedef struct _stritem {
2.    struct _stritem *next; //链表中下一个，这个链表有可能是slots链表，也有可能是LRU链表，但一个item不可能同时这两个链表中，所以复用一个指针。
3.    struct _stritem *prev; //链表中上一个。
4.    struct _stritem *h_next;  //相同hash值中链表的下一个。
5.    rel_time_t time;   //最近访问时间
6.    rel_time_t exptime;  //过期时间
7.    int nbytes;  //value的字节数
8.    unsigned short refcount; //引用计数
9.    uint8_t nsuffix;  //后缀长度
10.    uint8_t it_flags;  //标记
11.    uint8_t slabs_clsid;  //item所在的slabclass的id值
12.    uint8_t nkey; //键长
13.    /* this odd type prevents type-punning issues when we do
14.     * the little shuffle to save space when not using CAS. */
15.    union {
16.        uint64_t cas;
17.        char end;
18.    } data[]; //数据，这个数据不仅仅包括key对应的value，还有key、CAS、后缀等等数据也存在此，所以它有4部分“拼”成：CAS(可选)，KEY，后缀，VALUE。
19.    /* if it_flags & ITEM_CAS we have 8 bytes CAS */
20.    /* then null-terminated key */
21.    /* then " flags length\r\n" (no terminating null) */
22.    /* then data with terminating \r\n (no terminating null; it's binary!) */
23.} item;


c）head变量和tail变量

使用内存保存数据总会有满的情况，满就得淘汰，而memcached中的淘汰机制是LRU（最近最少使用算法 ），所以每个slabclass都保存着一个LRU队列，而head[i]和tail[i]则就是id为i的slabclass LRU队列的头部和尾部，尾部的item是最应该淘汰的项，也就是最近最少使用的项。



3）下面结合下面的结构图对memcached内存分配的模型进行解说：

a）初始化slabclass数组，每个元素slabclass[i]都是不同size的slabclass。

b）每开辟一个新的slab，都会根据所在的slabclass的size来分割chunk，分割完chunk之后，把chunk空间初始化成一个个free item，并插入到slot链表中。

c）我们每使用一个free item都会从slot链表中删除掉并插入到LRU链表相应的位置。

d）每当一个used item被访问的时候都会更新它在LRU链表中的位置，以保证LRU链表从尾到头淘汰的权重是由高到低的。

e）会有另一个叫“item爬虫”的线程（以后会讲到）慢慢地从LRU链表中去爬，把过期的item淘汰掉然后重新插入到slot链表中（但这种方式并不实时，并不会一过期就回收）。

f）当我们要进行内存分配时，例如一个SET命令，它的一般步骤是：

计算出要保存的数据的大小，然后选择相应的slabclass进入下面处理：

首先，从相应的slabclass LRU链表的尾部开始，尝试找几次（默认是5次），看看有没有过期的item（虽然有item爬虫线程在帮忙查找，但这里分配的时候，程序还是会尝试一下自己找，自己临时充当牛爬虫的角色），如果有就利用这个过期的item空间。

如果没找到过期的，则尝试去slot链表中拿空闲的free item。

如果slot链表中没有空闲的free item了，尝试申请内存，开辟一块新的slab，开辟成功后，slot链表就又有可用的free item了。

如果开不了新的slab那说明内存都已经满了，用完了，只能淘汰，所以用LRU链表尾部找出一个item淘汰之，并作为free item返回。

二）代码实现

从函数item_alloc说起，上一篇状态机文中也提到，如果是SET命令最终会来到item_alloc函数执行内存分配的工作，我们看下它的代码：
1.item *item_alloc(char *key, size_t nkey, int flags, rel_time_t exptime, int nbytes) {
2.    item *it;
3.    it = do_item_alloc(key, nkey, flags, exptime, nbytes, 0); //调用do_item_alloc
4.    return it;
5.}
6./**
7.item分配
8.把这个函数弄清楚，基本就把memcached内存管理机制大体弄清楚了。
9.*/
10.item *do_item_alloc(char *key, const size_t nkey, const int flags,
11.                    const rel_time_t exptime, const int nbytes,
12.                    const uint32_t cur_hv) {
13.    uint8_t nsuffix;
14.    item *it = NULL;
15.    char suffix[40];
16.    size_t ntotal = item_make_header(nkey + 1, flags, nbytes, suffix, &nsuffix); //item总大小
17.    if (settings.use_cas) {
18.        ntotal += sizeof(uint64_t); //如果有用到cas 那么item大小还要加上unit64_t的size
19.    }
20.    unsigned int id = slabs_clsid(ntotal); //根据item大小，找到适合的slabclass
21.    if (id == 0)
22.        return 0;
23.    mutex_lock(&cache_lock); //cache锁
24.    /* do a quick check if we have any expired items in the tail.. */
25.    /* 准备分配新的item了，随便快速瞄一下lru链表末尾有没有过期item，有的话就用过期的空间 */
26.    int tries = 5;
27.    int tried_alloc = 0;
28.    item *search;
29.    void *hold_lock = NULL;
30.    rel_time_t oldest_live = settings.oldest_live;
31.    search = tails[id]; //这个tails是一个全局变量，tails[xx]是id为xx的slabclass lru链表的尾部
32.    //从LRU链表尾部（就是最久没使用过的item）开始往前找
33.    for (; tries > 0 && search != NULL; tries--, search=search->prev) {
34.        if (search->nbytes == 0 && search->nkey == 0 && search->it_flags == 1) {
35.            /* We are a crawler, ignore it. */
36.            /*
37.                这里注释意思是说我们现在是以爬虫的身份来爬出过期的空间，
38.                像爬到这种异常的item，就别管了，不是爬虫要做的事，不要就行了。
39.             */
40.            tries++;
41.            continue;
42.        }
43.        /**
44.        你会看到很多地方有下面这个hv，在这先简单说下，也可先略过，其实它是对item的一个hash，得到hv值，这个hv主要有两个
45.        作用：
46.        1）用于hash表保存item，通过hv计算出哈希表中的桶号
47.        2）用于item lock表中锁住item，通过hv计算出应该用item lock表中哪个锁对当前item进行加锁
48.        这两者都涉及到一个粒度问题，不可能保证每个不一样的key的hv不会相同，所有hash方法都可能
49.        出现冲突。
50.        所以hash表中用链表的方式处理冲突的item，而item lock表中会多个item共享一个锁，或者说
51.        多个桶共享一个锁。
52.        */
53.        uint32_t hv = hash(ITEM_key(search), search->nkey);
54.        /* Attempt to hash item lock the "search" item. If locked, no
55.         * other callers can incr the refcount
56.         */
57.        /* Don't accidentally grab ourselves, or bail if we can't quicklock */
58.         /**
59.         尝试去锁住当前item。
60.         */
61.        if (hv == cur_hv || (hold_lock = item_trylock(hv)) == NULL)
62.            continue;
63.        if (refcount_incr(&search->refcount) != 2) {
64.            refcount_decr(&search->refcount);
65.            /* Old rare bug could cause a refcount leak. We haven't seen
66.             * it in years, but we leave this code in to prevent failures
67.             * just in case
68.            没看懂这里的意思.....
69.             */
70.            if (settings.tail_repair_time &&
71.                    search->time + settings.tail_repair_time < current_time) {
72.                itemstats[id].tailrepairs++;
73.                search->refcount = 1;
74.                do_item_unlink_nolock(search, hv);
75.            }
76.            if (hold_lock)
77.                item_trylock_unlock(hold_lock);
78.            continue;
79.        }
80.        /* Expired or flushed */
81.        //超时了...
82.        if ((search->exptime != 0 && search->exptime < current_time)
83.            || (search->time <= oldest_live && oldest_live <= current_time)) {
84.            itemstats[id].reclaimed++;
85.            if ((search->it_flags & ITEM_FETCHED) == 0) {
86.                itemstats[id].expired_unfetched++;
87.            }
88.            it = search; //拿下空间
89.            slabs_adjust_mem_requested(it->slabs_clsid, ITEM_ntotal(it), ntotal); //更新统计数据
90.            /**
91.            什么是link，在这简单说下，就是把item加到哈希表和LRU链表的过程。详见items::do_item_link函数 这里把item旧的link取消掉，当前函数do_item_alloc的工作只是拿空间，而往后可知道拿到item空间后会对这块item进行“link”工作，而这里这块item空间是旧的item超时然后拿来用的，所以先把它unlink掉
92.            */
93.            do_item_unlink_nolock(it, hv);
94.            /* Initialize the item block: */
95.            it->slabs_clsid = 0;
96.        } else if ((it = slabs_alloc(ntotal, id)) == NULL) {/*如果没有找到超时的item，则
97.                调用slabs_alloc分配空间，详见slabs_alloc
98.                如果slabs_alloc分配空间失败，即返回NULL，则往下走，下面的代码是
99.                把LRU列表最后一个给淘汰，即使item没有过期。
100.                这里一般是可用内存已经满了，需要按LRU进行淘汰的时候。
101.            */
102.            tried_alloc = 1; //标记一下，表示有进入此分支，表示有尝试过调用slabs_alloc去分配新的空间。
103.            //记下被淘汰item的信息，像我们使用memcached经常会查看的evicted_time就是在这里赋值啦！
104.            if (settings.evict_to_free == 0) {
105.                itemstats[id].outofmemory++;
106.            } else {
107.                itemstats[id].evicted++;
108.                itemstats[id].evicted_time = current_time - search->time; //被淘汰的item距离上次使用多长时间了
109.                if (search->exptime != 0)
110.                    itemstats[id].evicted_nonzero++;
111.                if ((search->it_flags & ITEM_FETCHED) == 0) {
112.                    itemstats[id].evicted_unfetched++;
113.                }
114.                it = search;
115.                slabs_adjust_mem_requested(it->slabs_clsid, ITEM_ntotal(it), ntotal);//更新统计数据
116.                do_item_unlink_nolock(it, hv); //从哈希表和LRU链表中删掉
117.                /* Initialize the item block: */
118.                it->slabs_clsid = 0;
119.                /*
120.                 在这也可以先略过下面的逻辑
121.                 如果当前slabclass有item被淘汰掉了，说明可用内存都满了，再也没有
122.                 slab可分配了，
123.                 而如果 slab_automove=2 (默认是1)，这样会导致angry模式，
124.                 就是只要分配失败了，就马上进行slab重分配：把别的slabclass空间牺牲
125.                 掉一些，马上给现在的slabclass分配空间，而不会合理地根据淘汰统计
126.                 数据来分析要怎么重分配（slab_automove = 1则会）。
127.                 */
128.                if (settings.slab_automove == 2)
129.                    slabs_reassign(-1, id);
130.            }
131.        }
132.        refcount_decr(&search->refcount);
133.        /* If hash values were equal, we don't grab a second lock */
134.        if (hold_lock)
135.            item_trylock_unlock(hold_lock);
136.        break;
137.    }
138.    /**
139.    如果上面的for循环里面没有找到空间，并且没有进入过else if ((it = slabs_alloc(ntotal, id)) == NULL)这个分支没有 尝试调slabs_alloc分配空间（有这种可能性），那么，下面这行代码就是再尝试分配。
140.    你会觉得上面那个循环写得特纠结，逻辑不清，估计你也看醉了。其实整个分配原则是这样子：
141.    1）先从LRU链表找下看看有没有恰好过期的空间，有的话就用这个空间。
142.    2）如果没有过期的空间，就分配新的空间。
143.    3）如果分配新的空间失败，那么往往是内存都用光了，则从LRU链表中把最旧的即使没过期的item淘汰掉，空间分给新的item用。
144.    问题是：这个从“LRU链表找到的item”是一个不确定的东西，有可能这个item数据异常，有可能这个item由于与别的item共用锁的桶号
145.    这个桶被锁住了，所以总之各种原因这个item此刻不一定可用，因此用了一个循环尝试找几次（上面是5）。
146.    所以逻辑是：
147.    1）我先找5次LRU看看有没有可用的过期的item，有就用它。（for循环5次）
148.    2）5次没有找到可用的过期的item，那我分配新的。
149.    3）分配新的不成功，那我再找5次看看有没有可用的虽然没过期的item，淘汰它，把空间给新的item用。（for循环5次）
150.    那么这里有个问题，如果代码要写得逻辑清晰一点，我得写两个for循环，一个是为了第2）步前“找可用的过期的”item，
151.    一个是第2）步不成功后“找可用的用来淘汰的”空间。而且有重复的逻辑“找到可用的”，所以memcached作者就合在一起了，
152.    然后只能把第2）步也塞到for循环里面，确实挺尴尬的。。。估计memcached作者也写得很纠结。。。
153.    所以就很有可能出现5次都没找到可用的空间，都没进入过elseif那个分支就被continue掉了，为了记下有没有进过elseif
154.    分支就挫挫地用一个tried_alloc变量来做记号。。
155.    */
156.    if (!tried_alloc && (tries == 0 || search == NULL))
157.        it = slabs_alloc(ntotal, id);
158.    if (it == NULL) {
159.        itemstats[id].outofmemory++;
160.        mutex_unlock(&cache_lock);
161.        return NULL; //没错！会有分配新空间不成功，而且尝试5次淘汰旧的item也没成功的时候，只能返回NULL。。
162.    }
163.    assert(it->slabs_clsid == 0);
164.    assert(it != heads[id]);
165.    //来到这里，说明item分配成功，下面主要是一些初始化工作。
166.    /* Item initialization can happen outside of the lock; the item's already
167.     * been removed from the slab LRU.
168.     */
169.    it->refcount = 1; /* the caller will have a reference */
170.    mutex_unlock(&cache_lock);
171.    it->next = it->prev = it->h_next = 0;
172.    it->slabs_clsid = id;
173.    DEBUG_REFCNT(it, '*');
174.    it->it_flags = settings.use_cas ? ITEM_CAS : 0;
175.    it->nkey = nkey;
176.    it->nbytes = nbytes;
177.    memcpy(ITEM_key(it), key, nkey);
178.    it->exptime = exptime;
179.    memcpy(ITEM_suffix(it), suffix, (size_t)nsuffix);
180.    it->nsuffix = nsuffix;
181.    return it;
182.}


上面的代码基本的中心逻辑就是：

1）先从LRU链表找下看看有没有恰好过期的空间，有的话就用这个空间。

2）如果没有过期的空间，就分配新的空间。

3）如果分配新的空间失败，那么往往是内存都用光了，则从LRU链表中把最旧的即使没过期的item淘汰掉，空间分给新的item用。

而第2）步分配的新空间，通过slabs_alloc(ntotal, id)函数来完成，我们再来解剖一下这个函数的实现：
1.void *slabs_alloc(size_t size, unsigned int id) {
2.    void *ret;
3.    pthread_mutex_lock(&slabs_lock);
4.    ret = do_slabs_alloc(size, id);
5.    pthread_mutex_unlock(&slabs_lock);
6.    return ret;
7.}
8./**
9.根据item大小和slabsclass分配空间
10.*/
11.static void *do_slabs_alloc(const size_t size, unsigned int id) {
12.    slabclass_t *p;
13.    void *ret = NULL;
14.    item *it = NULL;
15.    if (id < POWER_SMALLEST || id > power_largest) { //默认最大是200，最小是1
16.        MEMCACHED_SLABS_ALLOCATE_FAILED(size, 0);
17.        return NULL;
18.    }
19.    p = &slabclass[id]; //slabclass是一个全局变量，是各个slabclass对象数组，在这取得当前id对应的slabclass
20.    assert(p->sl_curr == 0 || ((item *)p->slots)->slabs_clsid == 0);
21.    /*
22.    下面这个if的逻辑相当于：
23.    如果p->sl_curr==0，即slots链表中没有空闲的空间，则do_slabs_newslab分配新slab
24.    如果p->sl_curr==0，且do_slabs_newslab分配新slab失败，则进入if，ret = NULL，否则进入下面的elseif
25.    */
26.    if (! (p->sl_curr != 0 || do_slabs_newslab(id) != 0)) {
27.        /* We don't have more memory available */
28.        ret = NULL;
29.    } else if (p->sl_curr != 0) { //如果进入此分支是因为slots链表中还有空闲的空间
30.        /* return off our freelist */
31.        //把空闲的item分配出去
32.        it = (item *)p->slots;
33.        p->slots = it->next;
34.        if (it->next) it->next->prev = 0;
35.        p->sl_curr--;
36.        ret = (void *)it;
37.    }
38.    if (ret) {
39.        p->requested += size; //分配成功，记下已分配的字节数
40.        MEMCACHED_SLABS_ALLOCATE(size, id, p->size, ret);
41.    } else {
42.        MEMCACHED_SLABS_ALLOCATE_FAILED(size, id);
43.    }
44.    return ret;
45.}


do_slabs_alloc函数做的事情就是先从slot中找，没有可用的item的话就调用do_slabs_newslab函数开辟新的slab，当然如果开辟失败就返回NULL告诉上层说，已经满了，没新slab可以开了。我们进去看看do_slabs_newslab是怎么实现的：
1./**
2.为slabclass[id]分配新的slab，仅当当前的slabclass中slots没有空闲的空间才调用
3.此函数分配新的slab
4.*/
5.static int do_slabs_newslab(const unsigned int id) {
6.    slabclass_t *p = &slabclass[id];
7.    int len = settings.slab_reassign ? settings.item_size_max
8.        : p->size * p->perslab; //先判断是否开启了自定义slab大小，如果没有就按默认的，即p->size*p->perslab（<=1M）
9.    char *ptr;
10.    /**
11.    下面if的逻辑是：
12.        如果内存超出了限制，分配失败进入if，返回0
13.        否则调用grow_slab_list检查是否要增大slab_list的大小
14.            如果在grow_slab_list返回失败，则不继续分配空间，进入if，返回0
15.            否则分配空间memory_allocate，如果分配失败，同样进入if，返回0；
16.    */
17.    if ((mem_limit && mem_malloced + len > mem_limit && p->slabs > 0) ||
18.        (grow_slab_list(id) == 0) ||
19.        ((ptr = memory_allocate((size_t)len)) == 0)) {
20.        MEMCACHED_SLABS_SLABCLASS_ALLOCATE_FAILED(id);
21.        return 0;
22.    }
23.    memset(ptr, 0, (size_t)len); //清干净内存空间
24.    split_slab_page_into_freelist(ptr, id); //把新申请的slab放到slots中去
25.    p->slab_list[p->slabs++] = ptr; //把新的slab加到slab_list数组中
26.    mem_malloced += len; //记下已分配的空间大小
27.    MEMCACHED_SLABS_SLABCLASS_ALLOCATE(id);
28.    return 1;
29.}
30.//附上grow_slab_list函数的说明
31.static int grow_slab_list (const unsigned int id) {
32.    slabclass_t *p = &slabclass[id];
33.    /**
34.        p->slab_list是一个空间大小固定的数组，是数组！而list_size是这个数组分配的空间。
35.        p->slabs代表已经分配出去的slabs数
36.        而p->list_size代表可以用多少个slabs数
37.        所以当slabs等于list_size的时候代表这个slab_list已经满了，得增大空间。
38.    */
39.    if (p->slabs == p->list_size) {
40.        size_t new_size = (p->list_size != 0) ? p->list_size * 2 : 16;
41.        void *new_list = realloc(p->slab_list, new_size * sizeof(void *)); //
42.        if (new_list == 0) return 0;
43.        p->list_size = new_size;
44.        p->slab_list = new_list;
45.    }
46.    return 1;
47.}
48./**
49.分配内存空间
50.*/
51.static void *memory_allocate(size_t size) {
52.    void *ret;
53.    /**
54.    有两种分配策略
55.    1）如果是开启了内存预分配策略，则只需要从预分配好的内存块那里割一块出来。即进入下面的else分支
56.    2）如果没有开启预分配，则malloc分配内存
57.    关于预分配详见 slabs_init
58.    */
59.    if (mem_base == NULL) {
60.        ret = malloc(size); //在这里终于见到我们熟悉的malloc函数！！
61.    } else {
62.    //省略预分配逻辑
63.    }
64.    return ret;
65.}


do_slabs_newslab最终会调用我们熟悉的malloc函数申请slab内存空间，申请成功后执行split_slab_page_into_freelist函数把slab割成一块块chunk，并把chunk初始化成free item并加到slot中：
1./**
2.把整个slab打散成一个个（也叫chunk）放到相应的slots链表中
3.*/
4.static void split_slab_page_into_freelist(char *ptr, const unsigned int id) {
5.    slabclass_t *p = &slabclass[id];
6.    int x;
7.    for (x = 0; x < p->perslab; x++) {
8.        do_slabs_free(ptr, 0, id); //这个函数主要作用是让当前item空间可用，即加到slots链表中。
9.        ptr += p->size;
10.    }
11.}
12./**
13.这个函数的命名虽然叫do_slabs_free，听上去好像是释放空间，其实质是把空间变成可用。
14.怎样的空间才算可用？就是加到当前slabclass的slots链表中而已。
15.所以新申请的slab也会调用这个函数，让整个slab变为可用。
16.ps: 这个命名应该有历史原因，因为以前的memcached版本slots链表保存的是回收的item空间，而
17.现在保存的是所有可用的item空间。
18.*/
19.static void do_slabs_free(void *ptr, const size_t size, unsigned int id) {
20.    slabclass_t *p;
21.    item *it;
22.    assert(((item *)ptr)->slabs_clsid == 0);
23.    assert(id >= POWER_SMALLEST && id <= power_largest);
24.    if (id < POWER_SMALLEST || id > power_largest)
25.        return;
26.    MEMCACHED_SLABS_FREE(size, id, ptr);
27.    p = &slabclass[id];
28.    it = (item *)ptr;
29.    it->it_flags |= ITEM_SLABBED; //把item标记为slabbed状态
30.    it->prev = 0;
31.    it->next = p->slots; //插入到slots链表中
32.    if (it->next) it->next->prev = it;
33.    p->slots = it;
34.    p->sl_curr++; //空闲item数加1
35.    p->requested -= size;
36.    return;
37.}


至此，我们已经把“分配”item空间的工作说完了，但是分配完item空间之后实质还有一些”收尾工作”，不知道你是否还记得在上一篇状态机中也提到，我们的一个SET命令分成两部分，一部分是“命令”行，第二部分是“数据”行，而上面所提到的item空间分配工作都是完成“命令”行的工作，回忆一下，状态机在完成“SET命令”第二部分行为（即把value塞到了我们分配的item的data字段的value位置）的时候，收尾的时候会来到：
1.static void complete_nread_ascii(conn *c) {
2. //。。
3. ret = store_item(it, comm, c);
4. //。。
5.}


其实这个store_item会对这个item进行一些收尾工作：
1.enum store_item_type store_item(item *item, int comm, conn* c) {
2.    enum store_item_type ret;
3.    uint32_t hv;
4.    hv = hash(ITEM_key(item), item->nkey); //锁住item
5.    item_lock(hv);
6.    ret = do_store_item(item, comm, c, hv);
7.    item_unlock(hv);
8.    return ret;
9.}
10.enum store_item_type do_store_item(item *it, int comm, conn *c, const uint32_t hv) {
11.  //。。。
12.      do_item_link(it, hv);
13.  //。。。
14.}


上面的do_item_link函数引出了一个叫“link”，链接的概念，这个link的意思就是主要包括下面三部分：

a）改变一些统计数据

b）把item加到哈希表

c）把item插入到相应的slabclass lru链表中
1.int do_item_link(item *it, const uint32_t hv) {
2.    MEMCACHED_ITEM_LINK(ITEM_key(it), it->nkey, it->nbytes);
3.    assert((it->it_flags & (ITEM_LINKED|ITEM_SLABBED)) == 0);
4.    mutex_lock(&cache_lock);
5.    it->it_flags |= ITEM_LINKED;
6.    it->time = current_time;
7.    STATS_LOCK();
8.    stats.curr_bytes += ITEM_ntotal(it);
9.    stats.curr_items += 1;
10.    stats.total_items += 1;
11.    STATS_UNLOCK();
12.    /* Allocate a new CAS ID on link. */
13.    ITEM_set_cas(it, (settings.use_cas) ? get_cas_id() : 0);
14.    assoc_insert(it, hv); //插入哈希表
15.    item_link_q(it); //加入LRU链表
16.    refcount_incr(&it->refcount);
17.    mutex_unlock(&cache_lock);
18.    return 1;
19.}

