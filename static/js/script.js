// // Book render
//
// "use strict";
//
// document.onreadystatechange = function () {
//     if (document.readyState == "complete") {
//         window.reader = ePubReader("https://www.litres.ru/pub/t/67253804-Ahunzh_anova_R._Sh_Hre_Bil_Rd_Kunakta_Gos.epub", {
//             restore: true
//         });
//     }
// };
//
// // Span wrap
// function wrapWords(str, tmpl) {
//     return str.replace(/(?<!(<\/?[^>]*|&[^;]*))([^\s<]+)/g, '$1<span data-jbox-content="$2" class="word" style="cursor: pointer">$2</span>');
// }
//
// function wrapTest() {
//     let paragraphs, body, index;
//     body = document.getElementsByTagName("body");
//     paragraphs = document.querySelectorAll('p.b');
// // for (index = 0; index < paragraphs.length; ++index) {
// //     console.log(a[index]);
// // }
//
//     console.log(paragraphs);
// }
//
// setTimeout(wrapTest, 5000);
