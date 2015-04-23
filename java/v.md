/** 
     * Cache to support the object identity semantics of autoboxing for values between  
     * -128 and 127 (inclusive) as required by JLS. 
     * 
     * The cache is initialized on first usage. During VM initialization the 
     * getAndRemoveCacheProperties method may be used to get and remove any system 
     * properites that configure the cache size. At this time, the size of the 
     * cache may be controlled by the vm option -XX:AutoBoxCacheMax=<size>. 
     */  
  
    // value of java.lang.Integer.IntegerCache.high property (obtained during VM init)  
    private static String integerCacheHighPropValue;  
  
    static void getAndRemoveCacheProperties() {  
        if (!sun.misc.VM.isBooted()) {  
            Properties props = System.getProperties();  
            integerCacheHighPropValue =  
                (String)props.remove("java.lang.Integer.IntegerCache.high");  
            if (integerCacheHighPropValue != null)  
                System.setProperties(props);  // remove from system props  
        }  
    }  
  
    private static class IntegerCache {  
        static final int high;  
        static final Integer cache[];  
  
        static {  
            final int low = -128;  
  
            // high value may be configured by property  
            int h = 127;  
            if (integerCacheHighPropValue != null) {  
                // Use Long.decode here to avoid invoking methods that  
                // require Integer's autoboxing cache to be initialized  
                int i = Long.decode(integerCacheHighPropValue).intValue();  
                i = Math.max(i, 127);  
                // Maximum array size is Integer.MAX_VALUE  
                h = Math.min(i, Integer.MAX_VALUE - -low);  
            }  
            high = h;  
  
            cache = new Integer[(high - low) + 1];  
            int j = low;  
            for(int k = 0; k < cache.length; k++) //缓存区间数据  
                cache[k] = new Integer(j++);  
        }  
  
        private IntegerCache() {}  
    }  
  
    /** 
     * Returns a <tt>Integer</tt> instance representing the specified 
     * <tt>int</tt> value. 
     * If a new <tt>Integer</tt> instance is not required, this method 
     * should generally be used in preference to the constructor 
     * {@link #Integer(int)}, as this method is likely to yield 
     * significantly better space and time performance by caching 
     * frequently requested values. 
     * 
     * @param  i an <code>int</code> value. 
     * @return a <tt>Integer</tt> instance representing <tt>i</tt>. 
     * @since  1.5 
     */  
    public static Integer valueOf(int i) {  
        if(i >= -128 && i <= IntegerCache.high)  
            return IntegerCache.cache[i + 128];  
        else  
            return new Integer(i);  
    }  




package h;

public class test
{   
  public static void main(String[] args)   
  {   
    int a = 1000, b = 1000;   
    System.out.println(a == b);   
  
    Integer c = 1000, d = 1000;   
    System.out.println(c == d);   
  
    Integer e = 100, f = 100;   
    System.out.println(e == f);   
  }   
}   




 true
 false
 true


Boolean：(全部缓存)
Byte：(全部缓存)
Short(-128 — 127缓存)
Character(<= 127缓存)
Float(没有缓存)
Long(-128 — 127缓存)


﻿﻿﻿﻿﻿﻿Doulbe(没有缓存)