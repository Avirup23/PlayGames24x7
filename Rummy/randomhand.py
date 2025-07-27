from decks import Deck
from algo_minscore import mscore
from algo_mindist import mdist
import os
import csv
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

OUTPUT_DIR = 'data/'  # Set your output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)
iterations = 1000000

# Settings list
all_settings = [
    (10, 2, 1, 2, [], 60),
    (10, 2, 1, 3, [], 60),
    (13, 2, 2, 2, [('Pseq', 3), ('Iseq', 3)], 80),
    (13, 2, 2, 3, [('Pseq', 3), ('Iseq', 3)], 80),
]

# Worker function
def simulate_once(args):
    handsize, n, ndeck, njoker, rules, maxscore = args
    d = Deck(ndeck, njoker)
    wcj = d.draw_wcj()
    hands = [d.draw(handsize) for _ in range(n)]
    min_score = mscore(hands[0], wcj, rules, False, 0, maxscore=maxscore)

    return {
        'hand': ' '.join(str(i) for i in hands[0]),
        'wcj': wcj,
        'minscore': min_score,
        'handsize': handsize,
        'njoker': njoker
    }

# CSV append function
def append_to_csv(results, handsize, njoker):
    filename = f'{OUTPUT_DIR}{handsize}.hand.{njoker}.joker.csv'
    fieldnames = ['hand', 'wcj', 'minscore']
    write_header = not os.path.exists(filename)

    with open(filename, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for row in results:
            writer.writerow({key: row[key] for key in fieldnames})

# Main parallel execution
if __name__ == '__main__':
    pool = Pool(cpu_count())
    for settings in all_settings:
        handsize, n, ndeck, njoker, rules, maxscore = settings
        args = [settings] * iterations

        results_iter = pool.imap_unordered(simulate_once, args, chunksize=100)
        buffer = []
        with tqdm(total=iterations, desc=f"{handsize}-card {njoker}-joker") as pbar:
            for res in results_iter:
                buffer.append(res)
                if len(buffer) >= 1000:
                    append_to_csv(buffer, handsize, njoker)
                    buffer.clear()
                pbar.update(1)
            if buffer:
                append_to_csv(buffer, handsize, njoker)
    pool.close()
    pool.join()