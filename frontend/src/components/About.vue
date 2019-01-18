<template>
  <div class="about">
    <h1>About Wikiplate</h1>
      <p>Wikiplate は，キーワードを基に Wikipedia の記事テンプレートを生成する Web アプリケーションです．<br>
      主な利用場面として，Wikipedia Town をはじめとする記事執筆イベントを想定しています．</p>
    <h2>記事テンプレートとは</h2>
      <p>本アプリケーションにおける記事テンプレートとは，Wikipedia の記事における以下の部分です．</p>
      <ul>
      <li class="l-item">Infobox の種類</li>
        <p>Infobox とは記事の右上に表示される統計情報の表です．<br>本アプリケーションでは，執筆する記事に適切な Infobox の種類を推薦します．</p>
      <li class="l-item">章構成</li>
        <p>本アプリケーションでは，記事の章構成における大見出しを推薦します．<br>記事執筆イベントで章ごとに執筆を分担する場合に利用できます．</p>
      </ul>
    <h2>利用方法</h2>
      <ol>
      <li class="l-item">記事テンプレートの生成</li>
        <ul>
        <li>作成したい記事に関するキーワードを任意の数，本アプリケーションの右上の入力フォームに<span class="parts">「:」区切り</span>で入力し<span class="parts">「作成」</span>ボタンをクリックすると記事テンプレートの生成が開始されます．</li>
          <p>キーワード例）「岡山城」についての記事を作成する場合 -> 城:史跡:観光地</p>
        <li>記事テンプレートの生成が完了すると，<span class="parts">「記事テンプレート」</span>タブにて確認できます．</li>
        <li>本アプリケーションは，Wikipedia の記事執筆で利用されるマークアップ形式で記事テンプレートを出力するため，そのまま記事作成画面に貼り付けて利用できます．</li>
        </ul><br>
      <li class="l-item">類似記事の確認と記事テンプレートの修正</li>
        <ul>
        <li><span class="parts">「類似記事」</span>タブでは，記事テンプレート生成に利用された Wikipedia 上の既存記事を確認できます．</li>
        <li>類似記事は，Infobox ごとにまとめられており，各 Infobox の欄にある<span class="parts">「類似記事を表示」</span>をクリックすることで，その Infobox を利用している類似記事を一覧できます．</li>
        <li>各類似記事について，章構成も合わせて表示されるため，記事テンプレートの章構成を修正する際に参考にできます．</li>
        <li>記事テンプレートの Infobox を修正したい場合は，各 Infobox の欄にある<span class="parts">「記事テンプレート再生成」</span>をクリックすることで，その Infobox を利用している類似記事を用いて記事テンプレートを再生成できます．</li>
        </ul>
      </ol>
    <h2>記事テンプレート生成方法</h2>
      <p>本アプリケーションでは，以下の手順で記事テンプレートを生成しています．</p>
      <ol>
      <li class="l-item">Wikipedia 上の既存記事に対し，その記事の特徴を表す特徴語を選出</li>
      <li class="l-item">入力されたキーワードを特徴語として持っている既存記事を類似記事として抽出</li>
      <li class="l-item">類似記事を用いて Infobox，章構成を推薦</li>
      </ol>

  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .about {
    height: 100%;
  }
  p {
    padding: 0 2%;
  }
  h2 {
    color: #4ab;
    font-size: 22px;
    padding-bottom: 0.3em;
  }
  span.parts {
    color: #090;
    font-weight: bold;
  }
  li.l-item {
    font-weight: bold;
  }
</style>
