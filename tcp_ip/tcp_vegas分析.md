tcp拥塞算法vegas分析



主要思想 估计一段时间能够发送的数据量，然后和最终发送的数据量

如果预测要发送的数据没有被 发送，


认为是阻塞

这个阻塞状态 长时间了，就会减低速度，

slow start


但这样情况，就会发生 黑客被欺骗

linux vegas遇到异常()
使用经典newerno算法


tcp发送回填满网络队列，Vegas 试试 队列保持为空
最终


如何计算



struct vegas {
    u32 beg_snd_nxt;    /* right edge during last RTT */
    u32 beg_snd_una;    /* left edge  during last RTT */
    u32 beg_snd_cwnd;   /* saves the size of the cwnd */
    u8  doing_vegas_now;/* if true, do vegas for this RTT */
    u16 cntRTT;     /* # of RTTs measured within last RTT */
    u32 minRTT;     /* min of RTTs measured within last RTT (in usec) */
    u32 baseRTT;    /* the min of all Vegas RTT measurements seen (in usec) */
};

aseRTT/minRTT/cntRTT这三个值

其中minRTT和cntRTT在其他的地方还有更新



void tcp_vegas_pkts_acked(struct sock *sk, u32 cnt, s32 rtt_us)
{
    struct vegas *vegas = inet_csk_ca(sk);
    u32 vrtt;
 
    if (rtt_us < 0)
        return;
 
    /* Never allow zero rtt or baseRTT */
    vrtt = rtt_us + 1;
 
    /* Filter to find propagation delay: */
    if (vrtt < vegas->baseRTT)
        vegas->baseRTT = vrtt;
 
    /* Find the min RTT during the last RTT to find
     * the current prop. delay + queuing delay:
     */
    vegas->minRTT = min(vegas->minRTT, vrtt);
    vegas->cntRTT++;
}

然后注意一下doing_vegas_now这个域，这个域表示是否需要vegas算法,而这个域的设置在set_state回调中，通过这个域，可以说混合了基于延迟和丢包的算法(类似微软的CTCP):