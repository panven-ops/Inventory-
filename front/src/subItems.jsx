import React, { useState } from "react";

const LOW_STOCK = 3;

function QuantityControl({ subItem, categoryId, updateQuantity }) {
  const [inputVal, setInputVal] = useState("");
  const [inputMode, setInputMode] = useState(false);
  const qty = subItem.quantity;

  const applyChange = (val) => {
    const num = parseInt(val);
    if (isNaN(num)) return;
    const newQty = Math.max(0, qty + num);
    updateQuantity(categoryId, subItem.id, newQty);
    setInputVal("");
    setInputMode(false);
  };

  const qtyColor =
    qty === 0
      ? "text-red-500 font-medium"
      : qty <= LOW_STOCK
      ? "text-amber-500 font-medium"
      : "text-slate-800 font-medium";

  return (
    <div className="flex items-center gap-2">
      <button
        onClick={() => updateQuantity(categoryId, subItem.id, qty - 1)}
        disabled={qty === 0}
        className="w-6 h-6 flex items-center justify-center rounded-md border border-slate-200 text-slate-500 hover:border-indigo-300 hover:text-indigo-600 hover:bg-indigo-50 disabled:opacity-30 disabled:cursor-not-allowed transition-colors text-sm"
      >
        −
      </button>

      {/*INPUT MODE vs DISPLAY MODE*/}
      {inputMode ? (
        <input
          type="number"
          value={inputVal}
          onChange={(e) => setInputVal(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") applyChange(inputVal);
            if (e.key === "Escape") setInputMode(false);
          }}
          onBlur={() => applyChange(inputVal)}
          autoFocus
          placeholder="+/-"
          className="w-14 h-6 text-center text-sm border border-indigo-300 rounded-md focus:outline-none focus:border-indigo-500 bg-white"
        />
      ) : (
        <span
          onClick={() => setInputMode(true)}
          title="Click for manual input"
          className={`min-w-[28px] text-center cursor-pointer select-none ${qtyColor}`}
        >
          {qty}
        </span>
      )}

      {/* Plus button */}
      <button
        onClick={() => updateQuantity(categoryId, subItem.id, qty + 1)}
        className="w-6 h-6 flex items-center justify-center rounded-md border border-slate-200 text-slate-500 hover:border-indigo-300 hover:text-indigo-600 hover:bg-indigo-50 transition-colors text-sm"
      >
        +
      </button>

      {/*STOCK BADGES*/}
      {qty === 0 && (
        <span className="text-xs bg-red-50 text-red-600 px-2 py-0.5 rounded-full font-medium">
          Out of stock
        </span>
      )}
      {qty > 0 && qty <= LOW_STOCK && (
        <span className="text-xs bg-amber-50 text-amber-600 px-2 py-0.5 rounded-full font-medium">
          Low: {qty} left
        </span>
      )}
    </div>
  );
}

function SubItems({ categoryId, subItems, addSubItem, deleteSubItem, updateQuantity }) {
  const [newSubItem, setNewSubItem] = useState("");

  return (
    //SUBITEMS WRAPPER
    <div>
      {subItems.length === 0 && (
        <p className="text-sm text-slate-400 py-2">
          No products yet — add one below
        </p>
      )}

      {/*SUB-ITEM ROWS*/}
      <div className="flex flex-col">
        {subItems.map((sub) => (
          <div
            key={sub.id}
            className="flex items-center justify-between py-2 border-b border-slate-100 last:border-0 gap-3"
          >
            <span className="text-sm text-slate-700 flex-1">{sub.name}</span>

            {/*Quantity control*/}
            <QuantityControl
              subItem={sub}
              categoryId={categoryId}
              updateQuantity={updateQuantity}
            />

            {/*Delete button*/}
            <button
              onClick={() => deleteSubItem(categoryId, sub.id)}
              className="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-red-50 text-slate-300 hover:text-red-500 transition-colors text-sm ml-1"
              title="Delete product"
            >
              ✕
            </button>
          </div>
        ))}
      </div>

      {/*ADD SUB-ITEM ROW*/}
      <div className="flex gap-2 mt-3 pt-3 border-t border-slate-100">
        <input
          placeholder="New product..."
          value={newSubItem}
          onChange={(e) => setNewSubItem(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && newSubItem.trim()) {
              addSubItem(categoryId, newSubItem.trim());
              setNewSubItem("");
            }
          }}
          className="flex-1 h-9 px-3 text-sm border border-slate-200 rounded-lg bg-slate-50 text-slate-900 focus:outline-none focus:border-indigo-400 focus:bg-white"
        />
        <button
          onClick={() => {
            if (newSubItem.trim()) {
              addSubItem(categoryId, newSubItem.trim());
              setNewSubItem("");
            }
          }}
          className="h-9 px-3 text-sm border border-indigo-200 text-indigo-600 font-medium rounded-lg hover:bg-indigo-50 transition-colors whitespace-nowrap"
        >
          + Add
        </button>
      </div>

    </div>
  );
}


export default SubItems;
