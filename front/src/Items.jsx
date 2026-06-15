import React, { useState } from "react";
import { useAuth } from "./AuthContext";
import { useSubItems } from "./usesubItems";
import SubItems from "./subItems";

function Items({
  items,
  newItem,
  setNewItem,
  addItem,
  deleteItem,
  updateItem,
  skip,
  setSkip,
  limit,
  total,
  accessToken,
  refreshToken,
  setAccessToken,
}) {
  const [search, setSearch] = useState("");
  const [editId, setEditId] = useState(null);
  const [editText, setEditText] = useState("");
  const { logout } = useAuth();

  const {
    subItemsMap,
    openCategories,
    toggleCategory,
    addSubItem,
    deleteSubItem,
    updateQuantity,
  } = useSubItems({ accessToken, refreshToken, setAccessToken, logout });

  const filteredItems = Array.isArray(items)
    ? items.filter((item) =>
        item.name.toLowerCase().includes(search.toLowerCase())
      )
    : [];

return (
    <div className="min-h-screen bg-slate-50">

      {/*TOPBAR*/}
      <div className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-2xl mx-auto px-4 h-13 flex items-center justify-between" style={{height: "52px"}}>

          {/* Brand */}
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center text-white text-xs">
              ▦
            </div>
            <span className="text-sm font-medium text-slate-800">Inventory</span>
          </div>

          {/* Logout button */}
          <button
            onClick={logout}
            className="text-sm text-slate-500 hover:text-slate-800 border border-slate-200 rounded-lg px-3 py-1.5 hover:bg-slate-50 transition-colors"
          >
            Logout
          </button>
        </div>
      </div>

      {/*MAIN CONTENT*/}
      <div className="max-w-2xl mx-auto px-4 py-6">

        {/* Page title + counter */}
        <div className="mb-5">
          <h1 className="text-lg font-medium text-slate-900">Categories</h1>
          <p className="text-sm text-slate-500 mt-0.5">
            {total} {total === 1 ? "category" : "categories"} total
          </p>
        </div>

        {/*TOOLBAR — search + add*/}
        <div className="flex gap-2 mb-4">
          {/* Search — relative/absolute για το icon, ίδιο pattern με login */}
          <div className="relative flex-1">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">🔍</span>
            <input
              placeholder="Search categories..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full h-10 pl-9 pr-3 text-sm border border-slate-200 rounded-lg bg-white text-slate-900 focus:outline-none focus:border-indigo-400"
            />
          </div>
        </div>

        {/*Add new category*/}
        <div className="flex gap-2 mb-6">
          <input
            placeholder="New category name..."
            value={newItem}
            onChange={(e) => setNewItem(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter") addItem(); }}
            className="flex-1 h-10 px-3 text-sm border border-slate-200 rounded-lg bg-white text-slate-900 focus:outline-none focus:border-indigo-400"
          />
          <button
            onClick={addItem}
            className="h-10 px-4 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-colors whitespace-nowrap"
          >
            + Add category
          </button>
        </div>

        {/*ITEMS LIST*/}
        <div className="flex flex-col gap-2">
          {filteredItems.map((item) => (

            //CATEGORY CARD
            <div
              key={item.id}
              className={`bg-white rounded-xl border transition-colors ${
                openCategories[item.id]
                  ? "border-indigo-300 border-l-[3px] border-l-indigo-500"
                  : "border-slate-200"
              }`}
            >
              {/*CARD HEADER*/}
              <div className={`flex items-center justify-between px-4 py-3 cursor-pointer ${
                openCategories[item.id] ? "bg-slate-50" : "hover:bg-slate-50"
              }`}>

                <span
                  onClick={() => toggleCategory(item.id)}
                  className="flex items-center gap-2 flex-1"
                >
                  <span className={`text-slate-400 text-xs transition-transform ${
                    openCategories[item.id] ? "rotate-90" : ""
                  }`}>▶</span>
                  <span className="text-sm font-medium text-slate-800">{item.name}</span>
                  {subItemsMap[item.id] && (
                    <span className="text-xs bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded-full font-medium">
                      {subItemsMap[item.id].length} items
                    </span>
                  )}
                </span>

                {/*Edit/Delete*/}
                {editId === item.id ? (
                  <div
                    className="flex items-center gap-2"
                    onClick={(e) => e.stopPropagation()}
                  >
                    <input
                      value={editText}
                      onChange={(e) => setEditText(e.target.value)}
                      className="h-8 px-2 text-sm border border-indigo-300 rounded-lg focus:outline-none"
                      autoFocus
                    />
                    <button
                      onClick={() => { updateItem(item.id, editText); setEditId(null); }}
                      className="h-8 px-3 bg-indigo-600 text-white text-xs font-medium rounded-lg hover:bg-indigo-700"
                    >
                      Save
                    </button>
                    <button
                      onClick={() => setEditId(null)}
                      className="h-8 px-2 text-slate-400 hover:text-slate-600 text-xs"
                    >
                      Cancel
                    </button>
                  </div>
                ) : (
                  <div
                    className="flex items-center gap-1"
                    onClick={(e) => e.stopPropagation()}
                  >
                    {/*ICON BUTTONS*/}
                    <button
                      onClick={() => { setEditId(item.id); setEditText(item.name); }}
                      className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors"
                      title="Edit"
                    >
                      ✏️
                    </button>
                    <button
                      onClick={() => deleteItem(item.id)}
                      className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-red-50 text-slate-400 hover:text-red-500 transition-colors"
                      title="Delete"
                    >
                      🗑️
                    </button>
                  </div>
                )}
              </div>

              {/*ACCORDION CONTENT*/}
              {openCategories[item.id] && (
                <div className="border-t border-slate-100 px-4 py-3">
                  <SubItems
                    categoryId={item.id}
                    subItems={subItemsMap[item.id] || []}
                    addSubItem={addSubItem}
                    deleteSubItem={deleteSubItem}
                    updateQuantity={updateQuantity}
                  />
                </div>
              )}
            </div>
          ))}

          {filteredItems.length === 0 && (
            <div className="text-center py-12 text-slate-400 text-sm">
              {search ? "No categories match your search" : "No categories yet — add one above"}
            </div>
          )}
        </div>

        {/*PAGINATION */}
        <div className="flex items-center justify-between mt-6">
          <button
            onClick={() => setSkip((prev) => Math.max(prev - limit, 0))}
            disabled={skip === 0}
            className="h-9 px-4 text-sm border border-slate-200 rounded-lg text-slate-500 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            ← Prev
          </button>

          <span className="text-sm text-slate-500">
            Page {Math.floor(skip / limit) + 1} of {Math.ceil(total / limit) || 1}
          </span>

          <button
            onClick={() => setSkip((prev) => prev + limit)}
            disabled={skip + limit >= total}
            className="h-9 px-4 text-sm border border-slate-200 rounded-lg text-slate-500 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            Next →
          </button>
        </div>

      </div>
    </div>
  );
}

export default Items;
