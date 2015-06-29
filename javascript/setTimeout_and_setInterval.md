#理解javaScript 定时器

###js是单线程异步，


#参考overstatckflow 回帖



####Yes. A Timeout executes a certain amount of time after setTimeout() is called; an Interval executes a certain amount of time after the previous interval fired.

#####1.TimeOut挂载在是在settimeout时间之后运行

#####2.Interval 是在前一个interval执行后，再挂载

#####You will notice the difference if your doStuff() function takes a while to execute. For example, if we represent a call to setTimeout/setInterval with ., a firing of the timeout/interval with * and JavaScript code execution with [-----], the timelines look like:

你会发现两者不同，列入doStuff(),setTimeout/setInterval表现是运行用*表示，时间轴用 [---]表示


Timeout:

.    *  .    *  .    *  .    *  .
     [--]    [--]    [--]    [--]

Interval:

.    *    *    *    *    *    *
     [--] [--] [--] [--] [--] [--]



#####The next complication is if an interval fires whilst JavaScript is already busy doing something (such as handling a previous interval). In this case, the interval is remembered, and happens as soon as the previous handler finishes and returns control to the browser. So for example for a doStuff() process that is sometimes short ([-]) and sometimes long ([-----]):
#####发生了竞争的情况，JS在忙（例如前一个interval执行任务)
#####在这种情况，interval会被记录下来，当前一个interval执行任务完成，返回的时候，马上执行

        *    *    •    *    •    *    *
     [-]  [-----][-][-----][-][-]  [-]

##### represents an interval firing that couldn't execute its code straight away, and was made pending instead.
很明显interval 没有顺利执行下去,会被替代

#####So intervals try to ‘catch up’ to get back on schedule. But, they don't queue one on top of each other: there can only ever be one execution pending per interval. (If they all queued up, the browser would be left with an ever-expanding list of outstanding executions!)
intervals 试图获得流程控制权，但它不会获取队列中的头
几个 interval,一些来不及执行的回调会被丢弃


.    *    •    •    x    •    •    x
     [------][------][------][------]
#####x represents an interval firing that couldn't execute or be made pending, so instead was discarded.

#####If your doStuff() function habitually takes longer to execute than the interval that is set for it, the browser will eat 100% CPU trying to service it, and may become less responsive.

#####Which do you use and why?

#####Chained-Timeout gives a guaranteed slot of free time to the browser; Interval tries to ensure the function it is running executes as close as possible to its scheduled times, at the expense of browser UI availability.

#####I would consider an interval for one-off animations I wanted to be as smooth as possible, whilst chained timeouts are more polite for ongoing animations that would take place all the time whilst the page is loaded. For less demanding uses (such as a trivial updater firing every 30 seconds or something), you can safely use either.

#####In terms of browser compatibility, setTimeout predates setInterval, but all browsers you will meet today support both. The last straggler for many years was IE Mobile in WinMo <6.5, but hopefully that too is now behind us.

#####Hi taylorhakes,

#####I change the last exapme program like this:
    
    // Get the start of code execution
    var start = new Date();
    // Mimics a long running call for a number of milliseconds 
    function waitMilliseconds(milliseconds) {
    var start = +(new Date());
    while(start + milliseconds > +(new Date())) {}
    }
    
    var id = setInterval(function() {
    var current = new Date();
    console.log('setInterval executing: ' + (current - start));
    
    waitMilliseconds(1500);
    }, 100);
    
    console.log('wait 3 seconds to stop the interval');
    // 10 seconds later clear the interval
    setTimeout(function() {
    clearInterval(id);
    }, 3000);
    
###In fact it dose not exetue 30 times, but only 3 time:
 
####wait 3 seconds to stop the interval
####setInterval executing: 100 
####setInterval executing: 1604 
####setInterval executing: 3106 
####It's hard to say weather there is a execution "stack", but it has been proved that it can be canceled.
####http://javascript.info/tutorial/settimeout-setinterval