# Directory comparison

```shell
git clone <this respository>
```
```python
from search_folder import SearchFolder

SearchFolder.check('test/test_folder', 'test/real_folder')
print(SearchFolder.diff)

# result
"""
{'T': ['test/test_folder\\4\\test.txt', 'test/test_folder\\4', 'test/test_folder\\3\\3-1\\3-1-1.py', 'test/test_folder\\3\\3-1', 'test/test_folder\\1\\1-2.txt', 'test/test_folder\\2\\2-1\\2-1-1.txt'], 'R': ['test/real_folder\\1\\1-2.py', 'test/real_folder\\2\\2-1\\2-1-1.java'], 'X': ['test/real_folder\\3\\3-1.csv']}
"""
```

### 조건
- 상위 폴더만 달라진 경우 (이름, 경로 etc ..) 모든 파일과 폴더가 변경되는 것으로 가정
- 같은 포매터로 포맷한 것들만 유효한 결과값을 도출할 수 있음.
- .png .jpg 같이 비교할 수 없는 파일들에 대한 예외처리

### 테스트
```shell
python -m unittest .\test\test_search_folder.py
```