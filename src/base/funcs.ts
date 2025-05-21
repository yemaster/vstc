export function hashCode(str: string) {
    let hash = 0
    for (let i = 0; i < str.length; i++) {
        hash = ~~(((hash << 5) - hash) + str.charCodeAt(i))
    }
    return Math.abs(hash)
}

export function deepCopy<T>(source: T): T {
  // 处理原始值、null 和 undefined
  if (source === null || typeof source !== 'object') {
    return source;
  }

  // 处理日期对象
  if (source instanceof Date) {
    return new Date(source.getTime()) as T;
  }

  // 处理正则表达式对象
  if (source instanceof RegExp) {
    return new RegExp(source) as T;
  }

  // 处理 Map 对象
  if (source instanceof Map) {
    const copy = new Map();
    source.forEach((value, key) => {
      copy.set(key, deepCopy(value));
    });
    return copy as T;
  }

  // 处理 Set 对象
  if (source instanceof Set) {
    const copy = new Set();
    source.forEach(value => {
      copy.add(deepCopy(value));
    });
    return copy as T;
  }

  // 使用 WeakMap 记录已拷贝的对象，避免循环引用
  const cache = new WeakMap();
  
  function innerCopy(obj: any): any {
    // 检查是否已拷贝过该对象
    if (cache.has(obj)) {
      return cache.get(obj);
    }

    // 创建新对象/数组，并指定正确类型
    const target: Record<string, any> = Array.isArray(obj) ? [] : {};
    cache.set(obj, target);

    // 递归拷贝所有属性
    Object.keys(obj).forEach(key => {
      const value = obj[key];
      target[key] = typeof value === 'object' && value !== null ? innerCopy(value) : value;
    });

    // 保留 Symbol 类型的属性
    Object.getOwnPropertySymbols(obj).forEach(sym => {
      const value = obj[sym];
      target[sym as any] = typeof value === 'object' && value !== null ? innerCopy(value) : value;
    });

    return target;
  }

  return innerCopy(source);
}
