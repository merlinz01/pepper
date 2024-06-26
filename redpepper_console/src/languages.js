const ace_languages = [
  // Common languages
  { id: 'plain_text', name: 'Plain Text', ext: ['txt'] },
  { id: 'c_cpp', name: 'C/C++', ext: ['c', 'cpp', 'h', 'hpp'] },
  { id: 'csharp', name: 'C#', ext: ['cs'] },
  { id: 'css', name: 'CSS', ext: ['css'] },
  { id: 'golang', name: 'Go', ext: ['go'] },
  { id: 'html', name: 'HTML', ext: ['html', 'htm'] },
  { id: 'ini', name: 'INI', ext: ['ini'] },
  { id: 'javascript', name: 'JavaScript', ext: ['js'] },
  { id: 'java', name: 'Java', ext: ['java'] },
  { id: 'json', name: 'JSON', ext: ['json'] },
  { id: 'json5', name: 'JSON5', ext: ['json5'] },
  { id: 'lua', name: 'Lua', ext: ['lua'] },
  { id: 'makefile', name: 'Makefile', filenames: ['makefile'], ext: ['mk', 'mak'] },
  { id: 'markdown', name: 'Markdown', ext: ['md', 'markdown'] },
  { id: 'properties', name: 'Properties', ext: ['properties', 'conf'] },
  { id: 'python', name: 'Python', ext: ['py', 'pyi', 'pyw'] },
  { id: 'ruby', name: 'Ruby', ext: ['rb'] },
  { id: 'rust', name: 'Rust', ext: ['rs'] },
  { id: 'sh', name: 'Shell', ext: ['sh'] },
  { id: 'sql', name: 'SQL', ext: ['sql'] },
  { id: 'toml', name: 'TOML', ext: ['toml'] },
  { id: 'typescript', name: 'TypeScript', ext: ['ts'] },
  { id: 'xml', name: 'XML', ext: ['xml'] },
  { id: 'yaml', name: 'YAML', ext: ['yaml', 'yml'] },
  // Less common languages
  { id: 'abap', name: 'ABAP' },
  { id: 'abc', name: 'ABC' },
  { id: 'actionscript', name: 'ActionScript' },
  { id: 'ada', name: 'Ada' },
  { id: 'alda', name: 'Alda' },
  { id: 'apache_conf', name: 'Apache Conf' },
  { id: 'apex', name: 'Apex' },
  { id: 'applescript', name: 'AppleScript' },
  { id: 'aql', name: 'AQL' },
  { id: 'asciidoc', name: 'AsciiDoc' },
  { id: 'asl', name: 'ASL' },
  { id: 'assembly_arm32', name: 'Assembly ARM32' },
  { id: 'assembly_x86', name: 'Assembly x86' },
  { id: 'astro', name: 'Astro' },
  { id: 'autohotkey', name: 'AutoHotkey' },
  { id: 'batchfile', name: 'BatchFile' },
  { id: 'bibtex', name: 'BibTeX' },
  { id: 'c9search', name: 'C9Search' },
  { id: 'cirru', name: 'Cirru' },
  { id: 'clojure', name: 'Clojure' },
  { id: 'cobol', name: 'COBOL' },
  { id: 'coffee', name: 'CoffeeScript' },
  { id: 'coldfusion', name: 'ColdFusion' },
  { id: 'crystal', name: 'Crystal' },
  { id: 'csound_document', name: 'Csound Document' },
  { id: 'csound_orchestra', name: 'Csound Orchestra' },
  { id: 'csound_score', name: 'Csound Score' },
  { id: 'csp', name: 'CSP' },
  { id: 'curly', name: 'Curly' },
  { id: 'cuttlefish', name: 'Cuttlefish' },
  { id: 'd', name: 'D' },
  { id: 'dart', name: 'Dart' },
  { id: 'diff', name: 'Diff' },
  { id: 'django', name: 'Django' },
  { id: 'dockerfile', name: 'Dockerfile', filenames: ['dockerfile'] },
  { id: 'dot', name: 'Dot' },
  { id: 'drools', name: 'Drools' },
  { id: 'edifact', name: 'EDIFACT' },
  { id: 'eiffel', name: 'Eiffel' },
  { id: 'ejs', name: 'EJS' },
  { id: 'elixir', name: 'Elixir' },
  { id: 'elm', name: 'Elm' },
  { id: 'erlang', name: 'Erlang' },
  { id: 'flix', name: 'Flix' },
  { id: 'forth', name: 'Forth' },
  { id: 'fortran', name: 'Fortran' },
  { id: 'fsharp', name: 'F#' },
  { id: 'fsl', name: 'FSL' },
  { id: 'ftl', name: 'FreeMarker' },
  { id: 'gcode', name: 'Gcode', ext: ['gcode', 'ngc'] },
  { id: 'gherkin', name: 'Gherkin' },
  { id: 'gitignore', name: 'Gitignore', filenames: ['.gitignore'] },
  { id: 'glsl', name: 'Glsl' },
  { id: 'gobstones', name: 'Gobstones' },
  { id: 'graphqlschema', name: 'GraphQLSchema' },
  { id: 'groovy', name: 'Groovy' },
  { id: 'haml', name: 'HAML' },
  { id: 'handlebars', name: 'Handlebars' },
  { id: 'haskell', name: 'Haskell' },
  { id: 'haskell_cabal', name: 'Haskell Cabal' },
  { id: 'haxe', name: 'Haxe' },
  { id: 'hjson', name: 'Hjson' },
  { id: 'html_elixir', name: 'HTML Elixir' },
  { id: 'html_ruby', name: 'HTML Ruby' },
  { id: 'io', name: 'Io' },
  { id: 'ion', name: 'Ion' },
  { id: 'jack', name: 'Jack' },
  { id: 'jade', name: 'Jade' },
  { id: 'jexl', name: 'JEXL' },
  { id: 'jsoniq', name: 'JSONiq' },
  { id: 'jsp', name: 'JSP' },
  { id: 'jssm', name: 'JSSM' },
  { id: 'jsx', name: 'JSX' },
  { id: 'julia', name: 'Julia' },
  { id: 'kotlin', name: 'Kotlin' },
  { id: 'latex', name: 'LaTeX' },
  { id: 'latte', name: 'Latte' },
  { id: 'less', name: 'LESS' },
  { id: 'liquid', name: 'Liquid' },
  { id: 'lisp', name: 'Lisp' },
  { id: 'livescript', name: 'LiveScript' },
  { id: 'logiql', name: 'LogiQL' },
  { id: 'lsl', name: 'LSL' },
  { id: 'luapage', name: 'LuaPage' },
  { id: 'lucene', name: 'Lucene' },
  { id: 'mask', name: 'Mask' },
  { id: 'matlab', name: 'MATLAB' },
  { id: 'maze', name: 'Maze' },
  { id: 'mediawiki', name: 'MediaWiki' },
  { id: 'mel', name: 'MEL' },
  { id: 'mips', name: 'MIPS' },
  { id: 'mixal', name: 'MIXAL' },
  { id: 'mushcode', name: 'MUSHCode' },
  { id: 'mysql', name: 'MySQL' },
  { id: 'nasal', name: 'Nasal' },
  { id: 'nginx', name: 'Nginx', ext: ['nginx'] },
  { id: 'nim', name: 'Nim' },
  { id: 'nix', name: 'Nix' },
  { id: 'nsis', name: 'NSIS', ext: ['nsis'] },
  { id: 'nunjucks', name: 'Nunjucks' },
  { id: 'objectivec', name: 'Objective-C' },
  { id: 'ocaml', name: 'OCaml' },
  { id: 'odin', name: 'Odin' },
  { id: 'partiql', name: 'PartiQL' },
  { id: 'pascal', name: 'Pascal' },
  { id: 'perl', name: 'Perl', ext: ['pl', 'pm'] },
  { id: 'pgsql', name: 'pgSQL' },
  { id: 'php', name: 'PHP', ext: ['php'] },
  { id: 'php_laravel_blade', name: 'PHP Laravel Blade' },
  { id: 'pig', name: 'Pig' },
  { id: 'plsql', name: 'PLSQL' },
  { id: 'powershell', name: 'Powershell', ext: ['ps1'] },
  { id: 'praat', name: 'Praat' },
  { id: 'prisma', name: 'Prisma' },
  { id: 'prolog', name: 'Prolog' },
  { id: 'protobuf', name: 'Protobuf', ext: ['proto'] },
  { id: 'prql', name: 'PRQL' },
  { id: 'puppet', name: 'Puppet' },
  { id: 'qml', name: 'QML', ext: ['qml'] },
  { id: 'r', name: 'R' },
  { id: 'raku', name: 'Raku' },
  { id: 'razor', name: 'Razor' },
  { id: 'rdoc', name: 'RDoc' },
  { id: 'red', name: 'Red' },
  { id: 'redshift', name: 'Redshift' },
  { id: 'rhtml', name: 'RHTML' },
  { id: 'robot', name: 'Robot' },
  { id: 'rst', name: 'RST' },
  { id: 'sac', name: 'SAC' },
  { id: 'sass', name: 'Sass' },
  { id: 'scad', name: 'SCAD' },
  { id: 'scala', name: 'Scala' },
  { id: 'scheme', name: 'Scheme' },
  { id: 'scrypt', name: 'SCrypt' },
  { id: 'scss', name: 'SCSS', ext: ['scss'] },
  { id: 'sjs', name: 'SJS' },
  { id: 'slim', name: 'Slim' },
  { id: 'smarty', name: 'Smarty' },
  { id: 'snippets', name: 'Snippets' },
  { id: 'soy_template', name: 'Soy Template' },
  { id: 'space', name: 'Space' },
  { id: 'sparql', name: 'SPARQL' },
  { id: 'sqlserver', name: 'SQL Server' },
  { id: 'stylus', name: 'Stylus' },
  { id: 'svg', name: 'SVG', ext: ['svg'] },
  { id: 'swift', name: 'Swift' },
  { id: 'tcl', name: 'Tcl', ext: ['tcl'] },
  { id: 'terraform', name: 'Terraform' },
  { id: 'tex', name: 'Tex', ext: ['tex'] },
  { id: 'text', name: 'Text' },
  { id: 'textile', name: 'Textile' },
  { id: 'tsx', name: 'TSX' },
  { id: 'turtle', name: 'Turtle' },
  { id: 'twig', name: 'Twig' },
  { id: 'vala', name: 'Vala' },
  { id: 'vbscript', name: 'VBScript', ext: ['vbs'] },
  { id: 'velocity', name: 'Velocity' },
  { id: 'verilog', name: 'Verilog' },
  { id: 'vhdl', name: 'VHDL' },
  { id: 'visualforce', name: 'Visualforce' },
  { id: 'vue', name: 'Vue', ext: ['vue'] },
  { id: 'wollok', name: 'Wollok' },
  { id: 'xquery', name: 'XQuery' },
  { id: 'zeek', name: 'Zeek' },
  { id: 'zig', name: 'Zig', ext: ['zig'] }
]

export default ace_languages
