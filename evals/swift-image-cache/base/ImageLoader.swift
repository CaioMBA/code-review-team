import Foundation

struct ImageLoader {
    func load(_ url: URL) async throws -> Data {
        try await URLSession.shared.data(from: url).0
    }
}
