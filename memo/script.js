document.getElementById("addNoteButton").addEventListener("click", addNote);
document.getElementById("clearNotesButton").addEventListener("click", clearNotes);

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const lines = [];
let startNote = null;  // 最初のクリックされたメモを保持

// メモを追加する関数
function addNote() {
  const note = document.createElement("div");
  note.classList.add("note");
  note.id = `note${Date.now()}`;  // ユニークなIDを付けて重複を防ぐ
  note.style.top = "100px";
  note.style.left = "100px";
  note.draggable = true;

  const textarea = document.createElement("textarea");
  textarea.textContent = "新しいメモ";

  note.appendChild(textarea);
  canvas.appendChild(note);  // canvasに追加

  addDragAndDrop(note);
  addClickEvent(note);
}

// ドラッグ＆ドロップ機能を追加
function addDragAndDrop(note) {
  let offsetX, offsetY;

  note.addEventListener("dragstart", (e) => {
    offsetX = e.clientX - note.offsetLeft;
    offsetY = e.clientY - note.offsetTop;
    note.style.zIndex = 10;
  });

  note.addEventListener("dragend", () => {
    note.style.zIndex = "";
  });

  canvas.addEventListener("dragover", (e) => {
    e.preventDefault();
  });

  note.addEventListener("drag", (e) => {
    note.style.left = `${e.clientX - offsetX}px`;
    note.style.top = `${e.clientY - offsetY}px`;
  });
}

// メモをクリックして線を描く処理
function addClickEvent(note) {
  note.addEventListener("click", (e) => {
    if (startNote === null) {
      // 最初のメモをセット
      startNote = note;
      note.style.border = "2px solid blue"; // ハイライト（選択中のメモ）
    } else {
      const startRect = startNote.getBoundingClientRect();
      const endRect = note.getBoundingClientRect();

      // 2つ目のメモと線を繋ぐ
      const line = {
        start: startNote.id,
        end: note.id,
        x1: startRect.left + startRect.width / 2,
        y1: startRect.top + startRect.height / 2,
        x2: endRect.left + endRect.width / 2,
        y2: endRect.top + endRect.height / 2,
      };
      lines.push(line);
      drawLine(line);  // 線を描画
      startNote.style.border = "";  // ハイライトを解除
      startNote = null;  // 次のメモのためにstartNoteをリセット
    }
  });

  // 右クリックで線を削除
  note.addEventListener("contextmenu", (e) => {
    e.preventDefault();
    removeLinesConnectedTo(note.id);
  });
}

// 線を描画
function drawLine(line) {
  ctx.beginPath();
  ctx.moveTo(line.x1, line.y1);
  ctx.lineTo(line.x2, line.y2);
  ctx.strokeStyle = "black";
  ctx.lineWidth = 2;
  ctx.stroke();
}

// 特定のメモにつながる線を削除
function removeLinesConnectedTo(noteId) {
  for (let i = lines.length - 1; i >= 0; i--) {
    if (lines[i].start === noteId || lines[i].end === noteId) {
      lines.splice(i, 1);
    }
  }
  redrawLines();
}

// メモの移動後に線を描き直す
function redrawLines() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  lines.forEach((line) => {
    const startNote = document.getElementById(line.start);
    const endNote = document.getElementById(line.end);
    if (startNote && endNote) {
      const startRect = startNote.getBoundingClientRect();
      const endRect = endNote.getBoundingClientRect();
      line.x1 = startRect.left + startRect.width / 2;
      line.y1 = startRect.top + startRect.height / 2;
      line.x2 = endRect.left + endRect.width / 2;
      line.y2 = endRect.top + endRect.height / 2;
      drawLine(line);
    }
  });
}

// メモ帳を全削除する関数
function clearNotes() {
  const notes = document.querySelectorAll(".note");
  notes.forEach(note => note.remove());
  lines.length = 0; // すべての線も削除
  ctx.clearRect(0, 0, canvas.width, canvas.height); // キャンバスをクリア
}

// ページ読み込み時に既存のメモを復元
window.onload = function () {
  const savedNotes = JSON.parse(localStorage.getItem("notes")) || [];
  savedNotes.forEach((noteData) => {
    const note = document.createElement("div");
    note.classList.add("note");
    note.id = noteData.id;
    note.style.left = `${noteData.left}px`;
    note.style.top = `${noteData.top}px`;
    note.draggable = true;

    const textarea = document.createElement("textarea");
    textarea.textContent = noteData.text;
    note.appendChild(textarea);

    canvas.appendChild(note);
    addDragAndDrop(note);
    addClickEvent(note);
  });
};

// メモの状態を保存
window.onbeforeunload = function () {
  const notes = [];
  document.querySelectorAll(".note").forEach((note) => {
    const rect = note.getBoundingClientRect();
    notes.push({
      id: note.id,
      text: note.querySelector("textarea").value,
      left: rect.left,
      top: rect.top,
    });
  });
  localStorage.setItem("notes", JSON.stringify(notes));
};
