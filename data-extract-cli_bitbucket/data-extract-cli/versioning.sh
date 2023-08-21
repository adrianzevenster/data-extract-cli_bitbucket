#!/bin/bash

# To get this working, add the following to the first line or as the first word of your last commit before PR merge.
#
# For minor increase:
# '([minor])' or '([feature])'
# For patch increase:
# '([patch])' or '([bugfix])' or '([hotfix])'

lastVersion=''
version=''
major=''
minor=''
patch=''
parentPrefix=''
currentPrefix=''
prefix=''
message=''

getVersion() {
	prefix=$1

	# If the prefix equals any of these, increase the minor version
	if [[ $prefix = '([feature])' ]] || [[ $prefix = '([minor])' ]]
	then
		minor=$[$minor + 1]
		patch=0
	# Same as above, but increase the patch version
	elif [[ $prefix = '([bugfix])' ]] || [[ $prefix = '([hotfix])' ]] || [[ $prefix = '([master])' ]] || [[ $prefix = '([patch])' ]]
	then
		patch=$[$patch + 1]
	fi

	version="$major.$minor.$patch"
}

setVersion() {
	git tag $version
	git push origin --tags

	echo $version
}

# get the newest git semver tag
lastVersion=$(git tag | sort -r --version-sort | head -n1)
# split the version pieces into in array
IFS='.' read -ra semVerArr <<< "$lastVersion"

# set variables for major, minor, patch
counter=0
for i in "${semVerArr[@]}"; do
	counter=$[$counter + 1]

	if [ $counter = 1 ]
	then
		major=$i
	elif [ $counter = 2 ]
	then
		minor=$i
	else
		patch=$i
	fi
done

commit=$(git rev-parse HEAD)
parent=$(git log --pretty=%P -n 1 "$commit")
# get the first line of the last parent commit
parentPrefix=$(git log --oneline --format=%B -n 1 $parent | head -n 1)
# get the first word of the commit
parentPrefix=$(echo $parentPrefix | awk '{print $1;}')

# get the first line of the last commit
currentPrefix=$(git log --oneline --format=%B -n 1 $commit | head -n 1)
# get the first word of the commit
currentPrefix=$(echo $currentPrefix | awk '{print $1;}')

# If the current commit has a valid prefix to increase the version
if getVersion "$currentPrefix" && [[ "$version" != "$lastVersion" ]];
then
	setVersion
# If the parent commit has a valid prefix to increase the version
elif getVersion "$parentPrefix" && [[ "$version" != "$lastVersion" ]];
then
	setVersion
else
	exit 1
fi
