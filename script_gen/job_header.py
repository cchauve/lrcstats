def writeHeader(file):
        '''
        Write the generic header lines for PBS scripts
        '''
        line = "#!/bin/bash\n"
        file.write(line)

        # Specify the location of the epilogue script
        line = "#PBS -l epilogue=%s/scripts/epilogue.script\n" % (variables["lrcstats"])
        file.write(line)

        # Email to send info about jobs
        line = "#PBS -M %s\n" % ( variables["email"] )
        file.write(line)

        # Only send emails when jobs are done or aborted
        # Epilogue info all in one file
        line = "#PBS -m ea\n" \
                "#PBS -j oe\n"
        file.write(line)
