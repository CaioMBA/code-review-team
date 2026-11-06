import SwiftUI

struct FeedView: View {
    let paths: [String]
    var body: some View {
        List(paths, id: \.self) { path in
            FeedRow(path: path)
        }
    }
}

struct FeedRow: View {
    let path: String
    @State private var data: Data?
    var body: some View {
        Group {
            if let data, let img = UIImage(data: data) { Image(uiImage: img).resizable().scaledToFit() }
            else { ProgressView() }
        }
        .onAppear { ImageCache.shared.image(for: path) { data = $0 } }
    }
}