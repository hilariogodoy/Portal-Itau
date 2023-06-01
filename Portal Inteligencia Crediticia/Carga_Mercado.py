from waitress import serve
import Index
serve(Index.server, host='0.0.0.0', port=8052)