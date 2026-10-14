-- Put each calendar image (and the heading right above it) on its own
-- landscape page in the PDF; tag the phone screenshot so CSS can shrink it.
local function calendar_img(block)
  if block and block.t == "Para" and #block.content == 1 and block.content[1].t == "Image" then
    local img = block.content[1]
    if img.src:match("^calendar/") then return img end
  end
end

function Pandoc(doc)
  local out, i = {}, 1
  local blocks = doc.blocks
  while i <= #blocks do
    local b = blocks[i]
    local img = calendar_img(blocks[i + 1])
    if b.t == "Header" and img then
      table.insert(out, pandoc.Div({ b, blocks[i + 1] }, { class = "wide-page" }))
      i = i + 2
    else
      table.insert(out, b)
      i = i + 1
    end
  end
  doc.blocks = out
  return doc
end

function Image(img)
  if img.src:match("mobile%-baseline") then img.classes:insert("small-shot") end
  return img
end
