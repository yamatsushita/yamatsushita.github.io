// Progressive enhancement only: the site is fully usable with JavaScript off.
(function () {
  "use strict";

  // Mobile navigation toggle.
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");

  if (toggle && nav) {
    toggle.hidden = false;
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  // Client-side filtering of the publication list.
  var search = document.querySelector(".pub-search");
  if (!search) return;

  var counter = document.querySelector(".pub-count");
  var groups = Array.prototype.slice.call(document.querySelectorAll(".year-group"));
  var items = Array.prototype.slice.call(document.querySelectorAll(".pub"));
  var empty = document.querySelector(".empty-state");
  var total = items.length;

  items.forEach(function (item) {
    item.dataset.haystack = item.textContent.toLowerCase().replace(/\s+/g, " ");
  });

  function report(n) {
    if (counter) {
      counter.textContent = n === total ? total + " publications" : n + " of " + total + " publications";
    }
    if (empty) empty.hidden = n !== 0;
  }

  function apply() {
    var terms = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    var shown = 0;

    items.forEach(function (item) {
      var hay = item.dataset.haystack;
      var match = terms.every(function (t) {
        return hay.indexOf(t) !== -1;
      });
      item.hidden = !match;
      if (match) shown++;
    });

    groups.forEach(function (group) {
      var any = group.querySelector(".pub:not([hidden])");
      group.hidden = !any;
    });

    report(shown);
  }

  search.addEventListener("input", apply);
  search.addEventListener("search", apply);
  report(total);
})();
