// Admin ro'yxatlarida: qator belgilansa (checkbox), darhol "O'chirish" tugmasi chiqadi.
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('changelist-form');
    if (!form) return;

    var actionSelect = form.querySelector('select[name="action"]');
    // "delete_selected" harakati mavjudmi tekshiramiz
    var hasDelete = false;
    if (actionSelect) {
      for (var i = 0; i < actionSelect.options.length; i++) {
        if (actionSelect.options[i].value === 'delete_selected') { hasDelete = true; break; }
      }
    }
    if (!hasDelete) return;

    // Tugmani yaratamiz
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = '🗑️ Tanlanganlarni o\u2019chirish';
    btn.style.cssText =
      'position:fixed;bottom:24px;right:24px;z-index:1000;' +
      'background:#dc3545;color:#fff;border:none;border-radius:30px;' +
      'padding:14px 26px;font-size:15px;font-weight:600;cursor:pointer;' +
      'box-shadow:0 6px 20px rgba(0,0,0,.35);display:none;';
    document.body.appendChild(btn);

    function selectedCount() {
      return form.querySelectorAll('input[name="_selected_action"]:checked').length;
    }

    function refresh() {
      var n = selectedCount();
      if (n > 0) {
        btn.style.display = 'block';
        btn.textContent = '🗑️ ' + n + ' ta qatorni o\u2019chirish';
      } else {
        btn.style.display = 'none';
      }
    }

    // Har qanday checkbox o'zgarsa yangilaymiz
    form.addEventListener('change', function (e) {
      if (e.target && e.target.name === '_selected_action') refresh();
      if (e.target && e.target.id === 'action-toggle') setTimeout(refresh, 0);
    });
    form.addEventListener('click', function (e) {
      if (e.target && e.target.id === 'action-toggle') setTimeout(refresh, 0);
    });

    // Tugma bosilsa: delete_selected ni tanlab, formani yuboramiz
    btn.addEventListener('click', function () {
      if (selectedCount() === 0) return;
      actionSelect.value = 'delete_selected';
      var go = form.querySelector('button[name="index"], input[name="index"]');
      if (go) { go.click(); }
      else { form.submit(); }
    });

    refresh();
  });
})();
