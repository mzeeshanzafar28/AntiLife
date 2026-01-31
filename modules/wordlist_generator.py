import itertools

def generate_wordlist_logic(chars, min_line, max_len, output_file, update_callback=None, check_stop=None):
    """
    Generates a wordlist.
    update_callback: function(current_count)
    check_stop: function() returns True if should stop
    """
    count = 0
    try:
        with open(output_file, 'w') as f:
            for length in range(min_line, max_len + 1):
                for p in itertools.product(chars, repeat=length):
                    if check_stop and check_stop():
                        return "Stopped", count
                    
                    word = "".join(p)
                    f.write(word + "\n")
                    count += 1
                    
                    if update_callback and count % 1000 == 0:
                        update_callback(count)
    except Exception as e:
        return str(e), count
        
    return "Success", count
