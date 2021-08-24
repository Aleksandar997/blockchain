export class StorageHelper {

    static clearAllData() {
        sessionStorage.clear();
    }

    // session data
    static setData(name: string, data: any) {
        sessionStorage.setItem(name + '.CacheData', JSON.stringify(data));
    }
    static getData(name: string) {
        return JSON.parse(sessionStorage.getItem(name + '.CacheData') as string);
    }
    static deleteData(name: string) {
        sessionStorage.removeItem(name + '.CacheData');
    }

    // local data
    static setLocalData(name: string, data: any) {
        localStorage.setItem(name, JSON.stringify(data));
    }
    static getLocalData(name: string) {
        return JSON.parse(localStorage.getItem(name) as string);
    }
    static deleteLocalData(name: string) {
        localStorage.removeItem(name);
    }
}
