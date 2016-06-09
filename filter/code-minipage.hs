import Text.Pandoc
import Text.Pandoc.JSON

main = toJSONFilter addMinipages'

addMinipages' :: Pandoc -> Pandoc
addMinipages' = bottomUp addMinipages

addMinipages :: [Block] -> [Block]
addMinipages (CodeBlock attr code : xs)
  | not (beginsWithEndMinipage xs) =
            [ RawBlock (Format "latex") "\\begin{minipage}{\\linewidth}"
            , CodeBlock attr code
            , RawBlock (Format "latex") "\\end{minipage}" ]
            ++ addMinipages xs
addMinipages (x:xs) = x : addMinipages xs
addMinipages [] = []

beginsWithEndMinipage (RawBlock (Format "latex") "\\end{minipage}":_) = True
beginsWithEndMinipage _ = False

--https://github.com/jgm/pandoc/issues/703
