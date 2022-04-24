import time
import tqdm


def run(code, board, handle):
    with tqdm.tqdm(total=len(code)) as pbar:
        while True:
            if len(code) == 0:
                break
            while True:
                if board.write(handle, code[0]) == 0:
                    time.sleep(1)
                else:
                    code = code[1:]
                    pbar.update(1)
                    break
