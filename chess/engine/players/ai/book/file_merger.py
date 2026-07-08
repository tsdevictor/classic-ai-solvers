import glob
import os

output = open('openings2.txt', 'w')

path = 'original/'
for filename in glob.glob(os.path.join(path, '*.txt')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:  # open in readonly mode
        all_openings = []
        for line in f.readlines():
            # end = ' '
            # if '0-1' in line or '1/2-1/2' in line or '1-0' in line:
            #     end = '\n'
            # if line[0] != '[':
            #   output.write(line[:-1] + end)

            # only take the openings
            if line[0] == '1' and line[1] == '.':
                try:
                    all_openings.append(line)  # '[0:line.index('5.')] + '\n')
                except ValueError:
                    pass

        unique_openings = []
        [unique_openings.append(game) for game in all_openings if game not in unique_openings]

        unique_openings.sort()

        for game in unique_openings:
            output.write(game)

        f.close()

output.close()
