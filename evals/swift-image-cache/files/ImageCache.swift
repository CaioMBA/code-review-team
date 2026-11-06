import Foundation

final class ImageCache {
    static let shared = ImageCache()
    private var store: [String: Data] = [:]
    private var onUpdate: (() -> Void)?
    private let loader = ImageLoader()

    func image(for path: String, completion: @escaping (Data?) -> Void) {
        if let cached = store[path] {
            completion(cached)
            return
        }
        let url = URL(string: "https://cdn.example.com/" + path)!
        Task.detached {
            let data = try? await self.loader.load(url)
            self.store[path] = data
            completion(data)
        }
    }

    func observe(_ handler: @escaping () -> Void) {
        onUpdate = {
            self.store.removeAll(keepingCapacity: true)
            handler()
        }
    }
}