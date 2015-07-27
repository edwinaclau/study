
类名就是关于一个平台的类

  private static final boolean IS_ANDROID = isAndroid0();

    private static final boolean IS_WINDOWS = isWindows0();
    private static final boolean IS_ROOT = isRoot0();

    private static final int JAVA_VERSION = javaVersion0();


isWindows

isandroid

jdk的版本

真正的实现为PlatformDependent0类

Class.forName("", false, getSystemClassLoader());


 Unsafe的使用

在这个类中大量使用了unsafe的功能


     private static boolean hasUnsafe0() {
    boolean noUnsafe = SystemPropertyUtil.getBoolean("io.netty.noUnsafe", false);
    logger.debug("-Dio.netty.noUnsafe: {}", noUnsafe);
    
    if (isAndroid()) {
    logger.debug("sun.misc.Unsafe: unavailable (Android)");
    return false;
    }
    
    if (noUnsafe) {
    logger.debug("sun.misc.Unsafe: unavailable (io.netty.noUnsafe)");
    return false;
    }
    
    // Legacy properties
    boolean tryUnsafe;
    if (SystemPropertyUtil.contains("io.netty.tryUnsafe")) {
    tryUnsafe = SystemPropertyUtil.getBoolean("io.netty.tryUnsafe", true);
    } else {
    tryUnsafe = SystemPropertyUtil.getBoolean("org.jboss.netty.tryUnsafe", true);
    }
    
    if (!tryUnsafe) {
    logger.debug("sun.misc.Unsafe: unavailable (io.netty.tryUnsafe/org.jboss.netty.tryUnsafe)");
    return false;
    }
    
    try {
    boolean hasUnsafe = PlatformDependent0.hasUnsafe();
    logger.debug("sun.misc.Unsafe: {}", hasUnsafe ? "available" : "unavailable");
    return hasUnsafe;
    } catch (Throwable t) {
    return false;
    }
    }





       private static long maxDirectMemory0() {
    long maxDirectMemory = 0;
    try {
    // Try to get from sun.misc.VM.maxDirectMemory() which should be most accurate.
    Class<?> vmClass = Class.forName("sun.misc.VM", true, ClassLoader.getSystemClassLoader());
    Method m = vmClass.getDeclaredMethod("maxDirectMemory");
    maxDirectMemory = ((Number) m.invoke(null)).longValue();
    } catch (Throwable t) {
    // Ignore
    }
    
    if (maxDirectMemory > 0) {
    return maxDirectMemory;
    }
    
    try {
    // Now try to get the JVM option (-XX:MaxDirectMemorySize) and parse it.
    // Note that we are using reflection because Android doesn't have these classes.
    Class<?> mgmtFactoryClass = Class.forName(
    "java.lang.management.ManagementFactory", true, ClassLoader.getSystemClassLoader());
    Class<?> runtimeClass = Class.forName(
    "java.lang.management.RuntimeMXBean", true, ClassLoader.getSystemClassLoader());
    
    Object runtime = mgmtFactoryClass.getDeclaredMethod("getRuntimeMXBean").invoke(null);
    
    @SuppressWarnings("unchecked")
    List<String> vmArgs = (List<String>) runtimeClass.getDeclaredMethod("getInputArguments").invoke(runtime);
    for (int i = vmArgs.size() - 1; i >= 0; i --) {
    Matcher m = MAX_DIRECT_MEMORY_SIZE_ARG_PATTERN.matcher(vmArgs.get(i));
    if (!m.matches()) {
    continue;
    }
    
    maxDirectMemory = Long.parseLong(m.group(1));
    switch (m.group(2).charAt(0)) {
    case 'k': case 'K':
    maxDirectMemory *= 1024;
    break;
    case 'm': case 'M':
    maxDirectMemory *= 1024 * 1024;
    break;
    case 'g': case 'G':
    maxDirectMemory *= 1024 * 1024 * 1024;
    break;
    }
    break;
    }
    } catch (Throwable t) {
    // Ignore
    }
    
    if (maxDirectMemory <= 0) {
    maxDirectMemory = Runtime.getRuntime().maxMemory();
    logger.debug("maxDirectMemory: {} bytes (maybe)", maxDirectMemory);
    } else {
    logger.debug("maxDirectMemory: {} bytes", maxDirectMemory);
    }
    
    return maxDirectMemory;
    }