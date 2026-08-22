# you5248 VPM Listing

VRChat Creator Companion（VCC）から you5248 のパッケージを追加するためのリスティング。

## VCC への登録

VCC → **Settings** → **Packages** → **Add Repository** に次を貼る。

```
https://you5248.github.io/vpm-listing/index.json
```

登録すると、各プロジェクトの **Manage Project** からパッケージを追加できるようになる。

## 収録パッケージ

| パッケージ | 内容 |
|---|---|
| [`com.you5248.dhk-shaders`](https://github.com/you5248/dhk-shaders) | Unity ビルトイン（BiRP）向けの軽量 Standard 互換シェーダー。バイキュービックライトマップ / MonoSH / LOD Cross-Fade / パックマップ / VRC Light Volumes（拡散）。Quest 版同梱 |

> `com.you5248.mirror-with-switch` は第三者由来のアセットを含むため非公開リポジトリで管理しており、
> このリスティングには載せていない。導入は `git clone` で行う。

## 新しい版を出したときの更新手順

1. パッケージ側のリポジトリでリリースを作る（zip の**ルートに `package.json`** が来るように）

   ```sh
   git archive --format=zip -o com.you5248.xxx-1.2.3.zip HEAD
   gh release create v1.2.3 com.you5248.xxx-1.2.3.zip
   ```

2. このリポジトリで index.json を作り直して push

   ```sh
   python tools/build_index.py
   git commit -am "1.2.3 を追加"
   git push
   ```

`tools/build_index.py` は GitHub のリリースを走査し、zip の中の `package.json` を
そのまま版情報として展開する。`zipSHA256` は実際にダウンロードして計算するので、
手で書き写す必要はない。載せるリポジトリは同スクリプトの `PACKAGE_REPOS` に書く。
